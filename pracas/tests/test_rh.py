from datetime import date
import json
import pytest

from django.contrib.auth import get_user_model

from rest_framework import status

from model_mommy import mommy

from core.helper_functions import test_reverse as _

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

    response = client.get(
        _list(kwargs={'praca_pk': praca.pk}), content_type='application/json')

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

    response = client.post(
        _list(kwargs={'praca_pk': praca.pk}),
        data,
        content_type="application/json")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_persiste_um_recurso_humano_usando_POST_com_identificacao(_common_user,
                                                                  client):
    """
    Testa a persistencia de um Recurso Humano utilizando um usuário
    identificado
    """

    praca = mommy.make('Praca')

    data = json.dumps({
        'nome': 'Fulano Cicrano',
    })

    response = client.post(
        _list(kwargs={'praca_pk': praca.pk}),
        data,
        content_type="application/json")

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_persiste_um_recurso_humano_usando_POST_como_gestor(_common_user,
                                                            client):
    """
    Testa a persistencia de um Recurso Humano utilizando um usuário
    identificado como gestor de Praça
    """

    praca = mommy.make('Praca')
    gestor = mommy.make('Gestor', praca=praca, user=_common_user, atual=True)

    data = json.dumps({
        'nome': 'Fulano Cicrano',
    })

    response = client.post(
        _list(kwargs={'praca_pk': praca.pk}),
        data,
        content_type="application/json")

    assert response.status_code == status.HTTP_201_CREATED


def test_persiste_um_recurso_humano_usando_POST_como_gestor_MinC(_admin_user,
                                                                 client):
    """
    Testa a persistencia de um Recurso Humano utilizando um usuário
    identificado como gestor do Ministério
    """

    praca = mommy.make('Praca')

    data = json.dumps({
        'nome': 'Fulano Cicrano',
    })

    response = client.post(
        _list(kwargs={'praca_pk': praca.pk}),
        data,
        content_type="application/json")

    assert response.status_code == status.HTTP_201_CREATED


def test_retorna_a_lista_de_rh_de_uma_Praca(client):
    """
    Testa o retorno de uma lista dos Recursos Humanos de uma Praca
    """

    praca = mommy.make('Praca')
    mommy.make('Rh', praca=praca, _quantity=5)

    response = client.get(
        _list(kwargs={'praca_pk': praca.pk}), content_type="application/json")

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

    response = client.get(
        _praca_detail(kwargs={'pk': praca.pk}),
        content_type="application/json")

    assert response.data['rh']
    assert isinstance(response.data['rh'], list)
    assert len(response.data['rh']) == 5


def test_retorna_determinados_campos_em_lista(client):
    """
    Testa quais campos retornam quando da listagem de RH de uma Praça
    """

    fields = [
        'url', 'id_pub', 'nome', 'funcao', 'local_trabalho', 'data_entrada',
        'data_saida'
    ]

    praca = mommy.make('Praca')
    mommy.make('Rh', praca=praca, _fill_optional=['data_entrada'], _quantity=2)

    response = client.get(
        _praca_detail(kwargs={'pk': praca.pk}),
        content_type="application/json")

    for field in fields:
        assert field in response.data['rh'][0]
        del response.data['rh'][0][field]

    assert len(response.data['rh'][0]) == 0


def test_arquiva_um_RH_usando_DELETE_sem_identificao(client):
    """
    Testa arquivar o registro de um Recurso Humano utilizando DELETE no
    endpoint, não utilizando identificação.
    """

    praca = mommy.make('Praca')
    rh = mommy.make('Rh', praca=praca, _quantity=2)

    response = client.delete(
        _detail(kwargs={'praca_pk': praca.pk,
                        'pk': rh[0].pk}),
        content_type="application/json")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_arquiva_um_RH_usando_DELETE_com_identificao(_common_user, client):
    """
    Testa arquivar o registro de um Recurso Humano utilizando DELETE no
    endpoint, utilizando identificação.
    """

    praca = mommy.make('Praca')
    rh = mommy.make('Rh', praca=praca, _quantity=2)

    response = client.delete(
        _detail(kwargs={'praca_pk': praca.pk,
                        'pk': rh[0].pk}),
        content_type="application/json")

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_arquiva_um_RH_usando_DELETE_como_gestor(_common_user, client):
    """
    Testa arquivar o registro de um Recurso Humano utilizando DELETE no
    endpoint, como gestor da Praça.
    """

    praca = mommy.make('Praca')
    gestor = mommy.make('Gestor', praca=praca, user=_common_user, atual=True)
    rh = mommy.make('Rh', praca=praca, _quantity=2)

    from pracas.models import Rh

    response = client.delete(
        _detail(kwargs={'praca_pk': praca.pk,
                        'pk': rh[0].pk}),
        content_type="application/json")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Rh.objects.count() == 2


def test_arquiva_um_RH_usando_DELETE_como_gestor_MinC(_admin_user, client):
    """
    Testa arquivar o registro de um Recurso Humano utilizando DELETE no
    endpoint, como gestor do Ministério.
    """

    praca = mommy.make('Praca')
    rh = mommy.make('Rh', praca=praca, _quantity=2)

    from pracas.models import Rh

    response = client.delete(
        _detail(kwargs={'praca_pk': praca.pk,
                        'pk': rh[0].pk}),
        content_type="application/json")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Rh.objects.count() == 2


def test_arquiva_um_RH_usando_DELETE_fornecendo_data_de_saida(_common_user,
                                                              client):
    """
    Testa arquivar o registro de um Recurso Humano utilizando DELETE no
    endpoint
    """

    from datetime import datetime
    from pracas.models import Rh

    praca = mommy.make('Praca')
    gestor = mommy.make('Gestor', praca=praca, user=_common_user, atual=True)
    rh = mommy.make('Rh', praca=praca, _quantity=2)

    date = datetime.strptime('22062017', '%d%m%Y').date()
    data = json.dumps({"data_saida": date.isoformat()})

    response = client.delete(
        _detail(kwargs={'praca_pk': praca.pk,
                        'pk': rh[0].pk}),
        data,
        content_type="application/json")

    rh = Rh.objects.get(pk=rh[0].pk)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Rh.objects.count() == 2
    assert rh.data_saida == date


def test_retorna_a_lista_completa_de_RH_da_Praca(client):
    """
    Testa o retorno da lista de todo o Histórico de RH de uma determinada Praça
    """

    praca = mommy.make('Praca')
    rhs = mommy.make('Rh', praca=praca, _quantity=4)
    rhs_baixa = mommy.make(
        'Rh', praca=praca, _quantity=4, _fill_optional=['data_saida'])

    response = client.get(
        _list(kwargs={'praca_pk': praca.pk}), content_type="application/json")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 8


def test_exclui_o_registro_de_vinculo_de_RH(_common_user, client):
    """
    Testa a exclusão do registro de vinculo de um RH
    """

    praca = mommy.make('Praca')
    rh = mommy.make('Rh', praca=praca)
    gestor = mommy.make('Gestor', praca=praca, user=_common_user, atual=True)

    data = json.dumps({'excluir': True})

    response = client.delete(
        _detail(kwargs={'praca_pk': praca.pk,
                        'pk': rh.pk}),
        data,
        content_type="application/json")

    assert response.status_code == status.HTTP_204_NO_CONTENT

    from pracas.models import Rh
    assert Rh.objects.count() == 0


def test_retorna_apenas_os_vinculos_ativos_de_RH_no_endpoint_praca(client):
    """
    Testa o retorno apenas dos vinculos ativos quando recuperado o registro de
    uma Praça.
    """

    praca = mommy.make('Praca')
    rh = mommy.make('Rh', praca=praca, _quantity=5)

    rh[0].data_saida = date.today()
    rh[0].save()

    response = client.get(_praca_detail(kwargs={'pk': praca.pk}),
                          content_type="application/json")

    assert len(response.data['rh']) == 4


def test_edita_informacoes_de_um_RH_como_usuario_nao_autenticado(client):
    """
    Testa alterar as informações de um RH como usuário não autenticado
    """

    praca = mommy.make('Praca')
    rh = mommy.make('Rh', praca=praca)

    data = {'identidade': '5514142542'}

    response = client.patch(_detail(kwargs={'praca_pk': praca.pk, 'pk': rh.pk})
                            , data
                            , content_type="application/json")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_edita_informacoes_de_um_RH_como_usuario_sem_permissao(_common_user, client):
    """
    Testa alterar as informações de um RH como usuário autenticado,
    porém, sem permissões de gestor.
    """

    praca = mommy.make('Praca')
    rh = mommy.make('Rh', praca=praca)

    data = {'identidade': '5514142542'}

    response = client.patch(_detail(kwargs={'praca_pk': praca.pk, 'pk': rh.pk})
                            , data
                            , content_type="application/json")

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_edita_informacoes_de_um_RH_como_gestor_da_Praca(_common_user, client):
    """
    Testa alterar as informações de um RH como gestor da Praça
    """

    praca = mommy.make('Praca')
    gestor = mommy.make('Gestor', praca=praca, user=_common_user, atual=True)
    rh = mommy.make('Rh', praca=praca)

    data = json.dumps({'identificacao': '5514142542'})

    response = client.patch(_detail(kwargs={'praca_pk': praca.pk, 'pk': rh.pk})
                            , data
                            , content_type="application/json")

    data = json.loads(data)
    assert response.status_code == status.HTTP_200_OK
    assert set(data).issubset(response.data)
