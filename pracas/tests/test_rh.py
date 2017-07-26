import json
import pytest

from django.contrib.auth import get_user_model

from rest_framework import status

from model_mommy import mommy

from core.helper_functions import _

from authentication.tests.test_user import _common_user
from authentication.tests.test_user import _admin_user


User = get_user_model()
pytestmark = pytest.mark.django_db

_list = _('pracas:rh-list')
_detail = _('pracas:rh-detail')
_praca_list = _('pracas:praca-list')
_praca_detail = _('pracas:praca-detail')


def test_get_URL_OK_from_RH_endpoint(client):
    """
    Testa retornar 200 OK para a URL do endpoint que lista todos os Recursos
    Humanos de uma Praça
    """

    praca = mommy.make('Praca')

    response = client.get(_list(kwargs={'praca_pk': praca.pk}),
                          content_type='application/json')

    assert response.status_code == status.HTTP_200_OK


def test_persiste_um_recurso_humano_usando_POST_sem_identificacao(client):
    """
    Testa a persistencia de um Recurso Humano utilizando um usuário sem
    identificação
    """

    praca = mommy.make('Praca')

    data = json.dumps({
        'nome': 'Fulano Cicrano',
    })

    response = client.post(_list(kwargs={'praca_pk': praca.pk}),
                           data, content_type="application/json")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_persiste_um_recurso_humano_usando_POST_com_identificacao(_common_user, client):
    """
    Testa a persistencia de um Recurso Humano utilizando um usuário
    identificado
    """

    praca = mommy.make('Praca')

    data = json.dumps({
        'nome': 'Fulano Cicrano',
    })

    response = client.post(_list(kwargs={'praca_pk': praca.pk}),
                           data, content_type="application/json")

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_persiste_um_recurso_humano_usando_POST_como_gestor(_common_user, client):
    """
    Testa a persistencia de um Recurso Humano utilizando um usuário
    identificado como gestor de Praça
    """

    praca = mommy.make('Praca')
    gestor = mommy.make('Gestor', praca=praca, user=_common_user, atual=True)

    data = json.dumps({
        'nome': 'Fulano Cicrano',
    })

    response = client.post(_list(kwargs={'praca_pk': praca.pk}),
                           data, content_type="application/json")

    assert response.status_code == status.HTTP_201_CREATED


def test_persiste_um_recurso_humano_usando_POST_como_gestor_MinC(_admin_user, client):
    """
    Testa a persistencia de um Recurso Humano utilizando um usuário
    identificado como gestor do Ministério
    """

    praca = mommy.make('Praca')

    data = json.dumps({
        'nome': 'Fulano Cicrano',
    })

    response = client.post(_list(kwargs={'praca_pk': praca.pk}),
                           data, content_type="application/json")

    assert response.status_code == status.HTTP_201_CREATED


def test_retorna_a_lista_de_rh_de_uma_Praca(client):
    """
    Testa o retorno de uma lista dos Recursos Humanos de uma Praca
    """

    praca = mommy.make('Praca')
    mommy.make('Rh', praca=praca, _quantity=5)

    response = client.get(_list(kwargs={'praca_pk': praca.pk}),
                          content_type="application/json")

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data, list)
    assert len(response.data) == 5


def test_retorna_a_lista_de_rh_ao_consultar_uma_Praca(client):
    """
    Testa o retorno de uma lista dos Recursos Humanos de uma Praca ao utilizar
    o endpoint de Pracas
    """

    praca = mommy.make('Praca')
    mommy.make('Rh', praca=praca, _quantity=5)

    response = client.get(_praca_detail(kwargs={'pk': praca.pk}),
                          content_type="application/json")

    assert response.data['rh']
    assert isinstance(response.data['rh'], list)
    assert len(response.data['rh']) == 5


def test_retorna_determinados_campos_em_lista(client):
    """
    Testa quais campos retornam quando da listagem de RH de uma Praça
    """

    fields = ['url', 'id_pub', 'nome', 'funcao', 'local_trabalho',
              'data_entrada', 'data_saida']

    praca = mommy.make('Praca')
    mommy.make('Rh', praca=praca, _fill_optional=True)

    response = client.get(_list(kwargs={'praca_pk': praca.pk}),
                          content_type="application/json")

    for field in fields:
        assert field in response.data[0]
        del response.data[0][field]

    assert len(response.data[0]) == 0
