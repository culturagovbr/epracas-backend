import pytest
import json

from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.reverse import reverse

from model_mommy import mommy

from core.helper_functions import _

from authentication.tests.test_user import _admin_user
from authentication.tests.test_user import _common_user

from gestor.models import Gestor

User = get_user_model()
pytestmark = pytest.mark.django_db

_detail = _('gestor:gestor-detail')
"""
Metodo _detail() que retorna a URL gestor:gestor-detail.
Aceita parametros como kwargs.
"""

_list = _('gestor:gestor-list')
"""
Metodo _list() retorna a URL gestor:gestor-list
"""


def test_return_200_ok_gestor_endpoint(client):
    """
    Testa retorno 200 OK do endpoint dos Gestores
    """

    response = client.get(_list())
    assert response.status_code == status.HTTP_200_OK


def test_return_manager_data_from_endpoint(client):
    """
    Testa o retorno de informações sobre um gestor de uma Praça
    """

    praca = mommy.make('Praca')
    gestor = mommy.make('Gestor', praca=praca)

    response = client.get(_detail(kwargs={'pk': gestor.pk}))

    fields = ('url', 'id_pub', 'user_id_pub', 'nome', 'email', 'praca',
              'profile_picture_url')

    assert response.status_code == status.HTTP_200_OK
    for field in fields:
        assert field in response.data


def test_return_praca_information_on_a_gestor_view(client):
    """
    Testa o retorno de determinadas informações sobre uma Praça no registro do
    seu atual Gestor.
    """

    praca = mommy.make('Praca')
    gestor = mommy.make('Gestor', praca=praca)

    fields = ('nome', 'url', 'municipio', 'uf', 'regiao')

    response = client.get(_detail(kwargs={'pk': gestor.pk}))

    for field in fields:
        assert field in response.data['praca']


def test_return_a_praca_with_manager_information(client):
    """
    Testa o retorno de uma Praça com a informação do seu atual gestor
    """

    praca = mommy.make('Praca')
    user = mommy.make(User, full_name="Fulano")
    gestor = mommy.make('Gestor', atual=True, praca=praca, user=user)

    response = client.get(
        reverse('pracas:praca-detail', kwargs={'pk': praca.pk}))

    assert response.status_code == status.HTTP_200_OK
    assert 'gestor' in response.data
    assert 'nome' in response.data['gestor']


def test_return_only_the_current_praca_manager(client):
    """
    Testa o retorno apenas do atual gestor da Praça
    """

    praca = mommy.make('Praca')
    gestor = mommy.make('Gestor', praca=praca, atual=True)
    gestores = mommy.make('Gestor', praca=praca, _quantity=2)

    response = client.get(
        reverse('pracas:praca-detail', kwargs={'pk': praca.pk}))

    assert response.status_code == status.HTTP_200_OK
    assert 'nome' in response.data['gestor']


def test_return_all_managers_from_a_praca(client):
    """
    Testa o retorno de todos os gestores de uma determinada Praça
    """

    pracas = mommy.make('Praca', _quantity=2)
    gestores_praca_0 = mommy.make('Gestor', praca=pracas[0], _quantity=4)
    gestores_praca_1 = mommy.make('Gestor', praca=pracas[1], _quantity=2)

    response = client.get(_list() + '?praca={}'.format(pracas[0].pk))

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 4

    response = client.get(_list() + '?praca={}'.format(pracas[1].pk))

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2


@pytest.mark.skip
def test_persist_a_gestors_address(client):
    """
    Testa persistir o endereço de um gestor
    """

    gestor = {
        'nome': 'Fulano Cicrano',
        'endereco': 'Conj 10, Casa 19',
        'cidade': 'Altamira',
        'uf': 'pa',
        'regiao': 'N'
    }

    response = client.post(_list(), gestor, format='json')
    response_content = json.loads(bytes.decode(response.content))
    response_content.pop('id_pub')

    assert response.status_code == status.HTTP_201_CREATED

    assert gestor == response_content


@pytest.mark.skip
def test_update_a_gestors_address(client):
    """
    Testa atulizar o endereço de um gestor
    """

    gestor = {
        'nome': 'Fulano Cicrano',
        'endereco': 'Conj 10, Casa 19',
        'cidade': 'Altamira',
        'uf': 'pa',
        'regiao': 'N'
    }

    post = client.post(_list(), gestor, format='json')
    assert post.status_code == status.HTTP_201_CREATED

    id_pub = json.loads(bytes.decode(post.content)).pop('id_pub')

    update = client.put(
        _detail(kwargs={'pk': id_pub}),
        json.dumps({
            'nome': 'Fulano Cicrano',
            'endereco': 'Conj 11, Casa 20'
        }),
        format='json',
        content_type='application/json')
    update_content = bytes.decode(update.content)

    assert update.status_code == status.HTTP_200_OK
    assert 'Conj 11, Casa 20' in update_content


@pytest.mark.skip
def test_return_a_FQDN_URL_from_Gestor_method(client):
    """
    Testa retornar uma URL a partir de um metodo da classe Gestor.
    """

    gestor = mommy.make(Gestor, nome='Fulano Cicrano')
    url = reverse(
        'gestor:gestor-detail',
        kwargs={'pk': gestor.id_pub}, )
    response = client.get(url, format='json')
    gestor_url = gestor.get_absolute_url()

    assert response.status_code == status.HTTP_200_OK
    assert gestor_url == url


def test_end_manager_relation_with_a_Praca(client):
    """
    Testa finalizar a relação de um Gestor com sua Praça, sem utilizar
    credenciais de identificação
    """

    gestor = mommy.make('Gestor')
    url = reverse('gestor:gestor-detail', kwargs={'pk': gestor.id_pub})

    response = client.delete(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_a_manager_from_a_praca_with_credentials(_common_user, client):
    """
    Testa finalizar a gestão de um Gestor utilizando o perfil de gestor de
    Praça
    """

    praca = mommy.make('Praca')
    gestor = mommy.make('Gestor', praca=praca, user=_common_user, atual=True)

    response = client.delete(_detail(kwargs={'pk': gestor.pk}))

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_delete_a_manager_from_a_praca_with_MinC_credentials(_admin_user,
                                                             client):
    """
    Testa finalizar a gestão de um Gestor em uma Praça utilizando o perfil de
    gestor do Ministério
    """

    praca = mommy.make('Praca')
    gestor = mommy.make('Gestor', praca=praca)

    response = client.delete(_detail(kwargs={'pk': gestor.pk}))

    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.get(
        reverse('pracas:praca-detail', kwargs={'pk': praca.pk}))

    assert not response.data['gestor']


def test_delete_a_manager_from_a_praca_with_MinC_credentials(_admin_user,
                                                             client):
    """
    Testa o processo de arquivar um gestor. Este deve permanecer na base a fins
    de auditoria e histórico, porém, sem permissões sobre a Praça.
    """

    praca = mommy.make('Praca')
    user = mommy.make(User)
    gestor = mommy.make('Gestor', praca=praca, user=user, atual=True)

    response = client.delete(_detail(kwargs={'pk': gestor.pk}))

    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.get(
        reverse('pracas:praca-detail', kwargs={'pk': praca.pk}))

    assert not response.data['gestor']

    assert Gestor.objects.count() == 1


def test_list_only_managers_with_mandate(client):
    """
    Testa exibir todos os gestores, de todas as Praças com mandato ativo.
    """

    pracas = mommy.make('Praca', _quantity=2)
    gestor = mommy.make('Gestor', praca=pracas[0], atual=True)
    gestores = mommy.make('Gestor', _quantity=5)

    response = client.get(_list() + '?atual=true')

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
