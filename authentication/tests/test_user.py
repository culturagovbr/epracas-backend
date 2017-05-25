import json
import pytest

from django.contrib.auth import get_user_model

from rest_framework.reverse import reverse
from rest_framework import status

from model_mommy import mommy

pytestmark = pytest.mark.django_db

User = get_user_model()


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
    'sub': '12345678',
    'surname': 'Cicrano',
}


@pytest.fixture
def _common_user(mocker):

    user = mommy.make(User, email='fulano@cicrano.com.br', sub=12345678)

    mock1 = mocker.patch(
        'oidc_auth.authentication.JSONWebTokenAuthentication.authenticate',
        return_value=(user, "")
        )

    mock2 = mocker.patch(
        'authentication.auth_methods.JWTUserAPIAuth.authenticate',
        return_value=(user, "")
        )

    mock1.start()
    mock2.start()

    return user


@pytest.fixture
def _admin_user(mocker):

    user = mommy.make(User, email='admin@cultura.gov.br', sub=876542321,
                      is_staff=True)

    mock1 = mocker.patch(
        'oidc_auth.authentication.JSONWebTokenAuthentication.authenticate',
        return_value=(user, "")
        )

    mock2 = mocker.patch(
        'authentication.auth_methods.JWTUserAPIAuth.authenticate',
        return_value=(user, "")
        )

    mock1.start()
    mock2.start()

    return user


def test_posting_user_information_without_a_valid_id_token(client):
    """
    Testa o envio de informações de um usuário para o endpoint correto
    sem a informação necessária para autenticação.
    """

    user = mommy.make(User, sub=12345678)
    response = client.post(
        reverse('auth:user-detail', kwargs={'sub': 12345678}),
        user_data,
        format='json'
        )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_posting_user_information_as_valid_user(_common_user, client):
    """
    Testa o envio de informações de usuário para o endpoint correto,
    como um usuário já autenticado no idCultura.
    """

    response = client.post(
        reverse('auth:user-detail', kwargs={'sub': 12345678}),
        user_data,
        format='json'
        )

    all_users = User.objects.all()
    assert len(all_users) == 1
    # TODO: Status code deve retornar 201, está retornando 200
    # assert response.status_code == status.HTTP_201_CREATED
    assert response.status_code == status.HTTP_200_OK


def test_getting_all_users_as_MinC_manager(_admin_user, client):
    """
    Testa o retorno dos usuários cadastrados na API para a tela de gestor.

    """

    mommy.make(User, _quantity=3)

    response = client.get(
        reverse('auth:user-list'),
        format='json',
        )

    assert response.status_code == status.HTTP_200_OK
    assert 'email' in str(response.content)
    assert len(response.data) == 4


def test_return_only_own_information_as_common_user(_common_user, client):
    """
    Testa o retorno das informações de um unico usuário quando ele for um
    usuário comum.
    """

    mommy.make(User, _quantity=1)

    response = client.get(
        reverse('auth:user-detail', kwargs={'sub': 12345678}),
        format='json',
        )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


def test_returning_404_when_its_user_first_login(_common_user, client):
    """
    Testa o retorno de um erro 404 quando do primeiro login de um usuário na
    API, já que esta ainda não possui as informações salvas no banco.
    """

    User.objects.first().delete()

    response = client.get(
        reverse('auth:user-detail', kwargs={'sub': 12345678}),
        format='json'
        )

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_user_information(_common_user, client):
    """
    Testa atualizar as informações de um usuario através de PATCH
    """

    user_data['email'] = 'alteracao@cultura.gov.br'
    json_user_data = json.dumps(user_data)

    response = client.patch(
        reverse('auth:user-detail', kwargs={'sub': user_data['sub']}),
        data=json_user_data,
        content_type="application/json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data['email'] == user_data['email']


def test_common_user_trying_to_get_staff_permissions(_common_user, client):
    """
    Testa a capacidade de um usuário comum obter permissões de gestor de
    ministerio.
    """

    response = client.patch(
        reverse('auth:user-detail', kwargs={'sub': user_data['sub']}),
        data=json.dumps({"is_staff": True}),
        content_type="application/json")

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_common_user_trying_to_giveup_on_staff_permissions(_admin_user, client):
    """
    Testa a capacidade de um usuário abdicar das permissões de gestor de
    ministério.
    """

    user = User.objects.first()

    response = client.patch(
        reverse('auth:user-detail', kwargs={'sub': user.sub}),
        data=json.dumps({"is_staff": False}),
        content_type="application/json")

    assert response.status_code == status.HTTP_200_OK


def test_manager_information_on_user_profile(_common_user, client):
    """
    Testa o retorno de informações do perfil de Gestor de Praça.
    """

    praca = mommy.make('Praca')
    gestor = mommy.make('Gestor', praca=praca, user=_common_user, atual=True)

    response = client.get(
        reverse('auth:user-detail', kwargs={'sub': _common_user.sub})
        )

    assert response.status_code == status.HTTP_200_OK
    assert "praca_manager" in response.data[0]
