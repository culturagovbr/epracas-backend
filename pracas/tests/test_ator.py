import json
import pytest

from rest_framework import status

from model_mommy import mommy

from core.helper_functions import test_reverse as _

from authentication.tests.test_user import _common_user
from authentication.tests.test_user import _admin_user

pytestmark = pytest.mark.django_db

_list = _('pracas:ator-list')
_detail = _('pracas:ator-detail')
_praca_detail = _('pracas:praca-detail')


def test_retorna_200_OK_URL_endpoint_ator(client):
    """
    Testa retornar 200 OK para a URL do endpoint que lista todos os Atores
    de uma Praça
    """

    praca = mommy.make('Praca')

    response = client.get(
        _list(kwargs={'praca_pk': praca.pk}), content_type='application/json')

    assert response.status_code == status.HTTP_200_OK


def test_retorna_n_campos_ao_requisitar_uma_Praca(client):
    """
    Testa quais informações sobre atores retornam em uma requisição a uma Praça
    """

    praca = mommy.make('Praca')
    atores = mommy.make('Ator', praca=praca, _quantity=2)

    fields = ('nome', 'area', 'imagem')

    response = client.get(
        _praca_detail(kwargs={'pk': praca.pk}), content_type="application/json"
        )

    assert 'atores' in response.data
    for field in fields:
        assert field in response.data['atores'][0]


def test_retorna_n_campos_ao_requisitar_diretamente_um_ator(client):
    """
    Testa quais informações sobre atores retornam em uma requisição direta ao
    endpoint de Atores
    """

    praca = mommy.make('Praca')
    ator = mommy.make('Ator', praca=praca)

    fields = ('id_pub', 'nome', 'area', 'area_descricao', 'descricao',
              'descricao_descricao', 'endereco', 'telefone1',
              'telefone2', 'email', 'lat', 'long')

    response = client.get(
        _detail(kwargs={'praca_pk': praca.pk, 'pk': ator.pk}),
        content_type="application/json")

    assert response.status_code == status.HTTP_200_OK
    for field in fields:
        assert field in response.data


def test_persiste_um_ator_usando_POST(client):
    """
    Testa a persistencia de um Ator de uma Praça utilizando um usuário sem
    identificação
    """

    praca = mommy.make('Praca')

    data = json.dumps({
        'nome': 'Fulano Cicrano',
    })

    response = client.post(
        _list(kwargs={'praca_pk': praca.pk}),
        data,
        content_type="application/json")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_persiste_um_ator_usando_POST_com_cred_identificao(_common_user, client):
    """
    Testa a persistencia de um Ator de uma Praça utilizando um usuário com
    identificação
    """

    praca = mommy.make('Praca')

    data = json.dumps({
        'nome': 'Fulano Cicrano',
        'area': 'asso',
        'descricao': '1',
    })

    response = client.post(
        _list(kwargs={'praca_pk': praca.pk}),
        data,
        content_type="application/json")

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_persiste_um_ator_usando_POST_como_gestor_da_Praca(_common_user, client):
    """
    Testa a persistencia de um Ator de uma Praça utilizando um usuário com
    identificação de Gestor da Praça
    """

    praca = mommy.make('Praca')
    gestor = mommy.make('Gestor', praca=praca, user=_common_user, atual=True)

    data = json.dumps({
        'nome': 'Fulano Cicrano',
        'area': 'asso',
        'descricao': '1',
    })

    response = client.post(
        _list(kwargs={'praca_pk': praca.pk}),
        data,
        content_type="application/json")

    assert response.status_code == status.HTTP_201_CREATED


def test_persiste_um_ator_usando_POST_como_gestor_do_MinC(_admin_user, client):
    """
    Testa a persistencia de um Ator de uma Praça utilizando um usuário com
    identificação de Gestor da Praça
    """

    praca = mommy.make('Praca')

    data = json.dumps({
        'nome': 'Fulano Cicrano',
        'area': 'asso',
        'descricao': '1',
    })

    response = client.post(
        _list(kwargs={'praca_pk': praca.pk}),
        data,
        content_type="application/json")

    assert response.status_code == status.HTTP_201_CREATED


def test_retorna_somente_os_atores_de_uma_determinada_praca(client):
    """
    Testa o retorno dos atores de uma determinada Praça.
    """

    pracas = mommy.make('Praca', _quantity=2)

    atores_praca1 = mommy.make('Ator', praca=pracas[0], _quantity=2)
    atores_praca2 = mommy.make('Ator', praca=pracas[1], _quantity=3)

    response = client.get(_praca_detail(kwargs={'pk': pracas[0].pk}))
    assert len(response.data['atores']) == 2

    response = client.get(_praca_detail(kwargs={'pk': pracas[1].pk}))
    assert len(response.data['atores']) == 3


def test_exclui_um_ator_de_determinada_praca(client):
    """
    Testa a exclusão de um Ator de determinada Praça.
    """

    praca = mommy.make('Praca')

    atores = mommy.make('Ator', praca=praca, _quantity=2)

    response = client.delete(_detail(kwargs={'praca_pk': praca.pk, 'pk':
                                             atores[0].pk}))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_exclui_um_ator_de_determinada_praca_com_cred_identificacao(_common_user, client):
    """
    Testa a exclusão de um Ator de determinada Praça como um usuário
    identificado.
    """

    praca = mommy.make('Praca')

    atores = mommy.make('Ator', praca=praca, _quantity=2)

    response = client.delete(_detail(kwargs={'praca_pk': praca.pk, 'pk':
                                             atores[0].pk}))

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_exclui_um_ator_de_determinada_praca_como_gestor_de_praca(_common_user, client):
    """
    Testa a exclusão de um Ator de determinada Praça como Gestor da Praça.
    """

    praca = mommy.make('Praca')
    gestor = mommy.make('Gestor', praca=praca, user=_common_user, atual=True)

    atores = mommy.make('Ator', praca=praca, _quantity=2)

    response = client.delete(_detail(kwargs={'praca_pk': praca.pk, 'pk':
                                             atores[0].pk}))

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert praca.atores.count() == 1


def test_exclui_um_ator_de_determinada_praca_como_gestor_MinC(_admin_user, client):
    """
    Testa a exclusão de um Ator de determinada Praça como Gestor do MinC.
    """

    praca = mommy.make('Praca')

    atores = mommy.make('Ator', praca=praca, _quantity=2)

    response = client.delete(_detail(kwargs={'praca_pk': praca.pk, 'pk':
                                             atores[0].pk}))

    assert response.status_code == status.HTTP_204_NO_CONTENT
