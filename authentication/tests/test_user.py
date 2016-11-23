import json
import pytest

from django.contrib.auth import get_user_model

from rest_framework.reverse import reverse
from rest_framework import status

from requests import Response

from jwkest.jwk import RSAKey, KEYS
from jwkest.jws import JWS
from Cryptodome.PublicKey import RSA

from model_mommy import mommy

pytestmark = pytest.mark.django_db

User = get_user_model()
rsakey = RSA.generate(2048)
key = RSAKey(key=rsakey)

# keys = KEYS()
# keys.add({'key': key, 'kty': 'RSA', 'kid': key.id})


def make_jwt(payload):
    jws = JWS(payload, alg='RS256')
    return jws.sign_compact([key])


def make_id_token(sub,
                 iss='http://example.com',
                 aud='you',
                 exp=999999999999999,
                 iat=999999999999999,
                 **kwargs):
    return make_jwt(dict(
        iss=iss,
        aud=aud,
        exp=exp,
        iat=iat,
        sub=str(sub),
        **kwargs
        ))


user_data = {
    'email': 'fulano.cicrano@beltrano.com.br',
    'email_verified': 'true',
    'family_name': 'Cicrano',
    'first_name': 'Fulano',
    'full_name': 'Fulano Cicrano',
    'given_name': 'Fulano',
    'id': '304050',
    'name': 'Fulano Cicrano',
    'picture': 'http://example.com/profile/picture/304050.jpg',
    'profile_picture_url': 'http://example.com/profile/picture/304050.jpg',
    'sub': '102030',
    'surname': 'Cicrano',
}


class FakeRequests(object):
    def __init__(self):
        self.responses = {}

    def set_response(self, url, content, status_code=200):
        self.responses[url] = (status_code, json.dumps(content))

    def get(self, url, *args, **kwargs):
        wanted_response = self.responses.get(url)
        if not wanted_response:
            status_code, content = 404, ''
        else:
            status_code, content = wanted_response

        response = Response()
        response._content = content.encode('utf-8')
        response.status_code = status_code

        return response


@pytest.fixture
def authentication(mocker):

    def patch(thing_to_mock, **kwargs):
        patcher = mocker.patch(thing_to_mock, **kwargs)
        patched = patcher.start()
        return patched

    user = mommy.make(User, email='fulano@cicrano.com.br', sub="12345678")
    responder = FakeRequests()
    responder.set_response("http://example.com/.well-known/openid-configuration",
                                {"jwks_uri": "http://example.com/jwks",
                                 "issuer": "http://example.com",
                                 "userinfo_endpoint": "http://example.com/userinfo"})
    mock_get = patch('requests.get')
    mock_get.side_effect = responder.get
    import ipdb
    ipdb.set_trace()
    keys = KEYS()
    keys.add({'key': key, 'kty': 'RSA', 'kid': key.kid})
    patch('jwkest.jwk.request', return_value=mocker.Mock(status_code=200,
                                                  text=keys.dump_jwks()))
    # patch('jwkest.jwk.request', return_value={"status_code":
    #                                           status.HTTP_200_OK, "text": keys.dump_jwks()})

    return user


def test_posting_user_information_without_a_valid_id_token(client):
    """
    Testa o envio de informações de um usuário para o endpoint correto
    sem a informação necessária para autenticação.
    """
    response = client.post(
        reverse('auth:user-list'),
        user_data,
        format='json'
        )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.skip
def test_posting_user_information_with_a_valid_id_token(client):
    """
    Testa o envio de informações de usuário para o endpoint correto,
    utilizando o cabeçalho com identificação JWT.
    """
    id_token = make_id_token(user_data)
    auth = 'JWT {}'.format(id_token)

    response = client.post(
        reverse('auth:user-list'),
        user_data,
        HTTP_AUTHORIZATION=auth,
        format='json'
        )

    # import ipdb
    # ipdb.set_trace()
    # user_updated = User.objects.get(sub=102030)
    assert response.status_code == status.HTTP_201_CREATED
    # assert user_updated.email == user_data['email']


def test_getting_all_users_as_MinC_manager(authentication, client):
    """
    Testa o retorno dos usuários cadastrados na API para a tela de gestor.

    """

    auth = 'JWT ' + make_id_token(authentication.sub)
    response = client.get(
        reverse('auth:user-list'),
        format='json',
        HTTP_AUTHORIZATION=auth
        )

    # import ipdb
    # ipdb.set_trace()
    assert response.status_code == status.HTTP_200_OK
    assert 'email' in response.data
    assert response.data['email'] == 'fulano@cicrano.com'
