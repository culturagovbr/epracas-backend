import pytest
import json
import pendulum

from django.core.files import File
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.reverse import reverse

from model_mommy import mommy

from core.helper_functions import _

from pracas.models import Praca
from gestor.models import Gestor
from gestor.models import ProcessoVinculacao

from authentication.tests.test_user import _admin_user
from authentication.tests.test_user import _common_user

pytestmark = pytest.mark.django_db

_list = _('gestor:processovinculacao-list')
"""
Metodo _list() que retorna URL da View gestor:processovinculacao-list.

Returns:
    Retorna uma string contendo a URL construida com os parametros informados

"""

_detail = _('gestor:processovinculacao-detail')
"""
Metodo _detail() que retorna URL da View gestor:processovinculacao-detail.

Args:
    kwargs: Um dict contendo os parametros a serem utilizados na construção da
    URL.

Returns:
    Retorna uma string contendo a URL construida com os parametros informados

"""


@pytest.fixture
def _create_temporary_file(mocker):
    return mocker.Mock(spec=File, name='FileMock')


def test_return_200_OK_to_Processo_list_URL(client):
    """
    Testa retorno de status 200_OK para o endpoint de Processos de Vinculação
    """

    response = client.get(
        reverse('gestor:processovinculacao-list'), format='json')
    assert response.status_code == status.HTTP_200_OK


def test_persist_a_process_using_POST_without_credencials(client):
    """
    Testa a persistencia de um Processo de Vinculação, sem credenciais de
    identificação
    """

    praca = mommy.make(Praca)

    data = json.dumps({"praca": str(praca.id_pub)})

    response = client.post(
        reverse('gestor:processovinculacao-list'),
        data,
        content_type="application/json")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_persist_a_process_using_POST_as_common_user(_common_user, client):
    """
    Testa a persistencia de um Processo de Vinculação, utilizando credenciais
    de identificação
    """

    praca = mommy.make(Praca)

    data = json.dumps({"praca": str(praca.id_pub)})

    response = client.post(
        reverse('gestor:processovinculacao-list'),
        data,
        content_type="application/json")

    assert response.status_code == status.HTTP_201_CREATED


def test_persist_a_process_using_POST_as_admin_user(_admin_user, client):
    """
    Testa a persistencia de um Processo de Vinculação, utilizando credenciais
    de administrador
    """

    praca = mommy.make(Praca)

    data = json.dumps({"praca": str(praca.id_pub)})

    response = client.post(
        reverse('gestor:processovinculacao-list'),
        data,
        content_type="application/json")

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_update_a_process_using_PATCH_as_process_owner(_common_user, client):
    """
    Testa a atualização de informações de um Processo de Vinculação, utilizando
    credenciais de identificação
    """

    praca1 = mommy.make('Praca')
    praca2 = mommy.make('Praca')
    processo = mommy.make(
        'ProcessoVinculacao', user=_common_user, praca=praca1)

    data = json.dumps({'praca': str(praca2.id_pub)})

    response = client.patch(
        reverse(
            'gestor:processovinculacao-detail', kwargs={'pk': processo.pk}),
        data,
        content_type="application/json")

    assert response.status_code == status.HTTP_200_OK


def test_update_a_process_using_PATCH_as_admin_user(_admin_user, client):
    """
    Testa a atualização de informações de um Processo de Vinculação, utilizando
    credenciais de identificação
    """

    User = get_user_model()

    user = mommy.make(User)
    praca1 = mommy.make('Praca')
    praca2 = mommy.make('Praca')
    processo = mommy.make('ProcessoVinculacao', praca=praca1, user=user)

    data = json.dumps({'praca': str(praca2.id_pub)})

    response = client.patch(
        reverse(
            'gestor:processovinculacao-detail', kwargs={'pk': processo.pk}),
        data,
        content_type="application/json")

    assert response.status_code == status.HTTP_200_OK


def test_update_a_process_using_PATCH_as_diferent_user(_common_user, client):
    """
    Testa a atualização de informações de um Processo de Vinculação, utilizando
    credenciais de identificação diferente das que iniciaram o processo.
    """

    User = get_user_model()

    user = mommy.make(User)
    praca1 = mommy.make('Praca')
    praca2 = mommy.make('Praca')
    processo = mommy.make('ProcessoVinculacao', praca=praca1, user=user)

    data = json.dumps({'praca': str(praca2.id_pub)})

    response = client.patch(
        reverse(
            'gestor:processovinculacao-detail', kwargs={'pk': processo.pk}),
        data,
        content_type="application/json")

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_return_a_list_of_process(client):
    """
    Testa o retorno de uma lista com informações basicas sobre os Processos de
    Vinculação
    """

    praca = mommy.make('Praca')
    processo = mommy.make('ProcessoVinculacao', praca=praca)

    response = client.get(
        reverse('gestor:processovinculacao-list'), format='json')

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data, list)


def test_return_a_list_of_open_processes(client):
    """
    Testa o retorno de uma lista de processos abertos aguardando despacho do
    gestor do MinC.
    """

    praca = mommy.make('Praca')
    processo = mommy.make('ProcessoVinculacao', praca=praca)
    arquivos = mommy.make('ArquivosProcessoVinculacao', processo=processo,
                          verificado=True, _quantity=5)
    processo.aprovado = True
    processo.save()

    processos = mommy.make('ProcessoVinculacao', praca=praca, aprovado=False,
                           _quantity=5)

    response = client.get(f'{_list()}?aprovado=false')

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 5


def test_return_changes_on_status_processes(_admin_user, client):
    """
    Testa o retorno das mudanças na situacao do Processo de Vinculação.
    """

    praca = mommy.make('Praca')
    processo = mommy.make('ProcessoVinculacao', praca=praca)

    data = json.dumps({
        "situacao": "p",
        "descricao": "Documentação não legivel"
    })

    response = client.patch(_detail(kwargs={"pk": processo.pk}), 
                            data, content_type="application/json")

    assert response.status_code == status.HTTP_200_OK
    assert "situacao" in response.data['registro'][0]


def test_which_fields_returns_on_a_list_of_process(client):
    """
    Testa o retorno de determinados campos na lista de Processos de Vinculação
    """

    praca = mommy.make('Praca')
    processo = mommy.make('ProcessoVinculacao', praca=praca)

    fields = ('url', 'id_pub', 'praca', 'user', 'data_abertura',
              'data_finalizacao', 'finalizado')

    response = client.get(
        reverse('gestor:processovinculacao-list'), format='json')

    for field in fields:
        assert field in response.data[0]
        response.data[0].pop(field)

    assert len(response.data[0]) == 0


def test_returning_information_about_a_praca_on_a_process(client):
    """
    Testa o retorno de informações sobre a Praça em um Processo de Vinculação
    """

    praca = mommy.make('Praca')

    mommy.make('ProcessoVinculacao', praca=praca)

    fields = ('url', 'id_pub', 'nome', 'municipio', 'uf')
    response = client.get(
        reverse('gestor:processovinculacao-list'), format='json')

    for field in fields:
        assert field in response.data[0]['praca']


def test_returning_information_about_an_user_of_a_process(client):
    """
    Testa o retorno de informações publicas sobre o usuário que requisitou um
    Processo de Vinculação com uma Praça.
    """

    praca = mommy.make('Praca')

    mommy.make('ProcessoVinculacao', praca=praca)

    fields = ('full_name', 'profile_picture_url')
    response = client.get(
        reverse('gestor:processovinculacao-list'), format='json')

    for field in fields:
        assert field in response.data[0]['user']
        response.data[0]['user'].pop(field)

    # assert len(response.data[0]['praca']) == 0


def test_returning_information_about_an_user_of_a_process_detailed(_common_user, client):
    """
    Testa o retorno de informações sobre o usuário que requisitou um Processo
    de Vinculação com uma Praça.
    """

    praca = mommy.make('Praca')
    processo = mommy.make('ProcessoVinculacao', praca=praca, user=_common_user)

    fields = ('full_name',)
    response = client.get(
        reverse('gestor:processovinculacao-detail',
                kwargs={'pk': processo.pk}),
        format='json'
    )

    for field in fields:
        assert field in response.data['user']


def test_returning_fields_on_a_detailed_process_without_credentials(client):
    """
    Testa o retorno de informações detalhadas sobre um Processo de Vinculação,
    não utilizando credencial de identificação.
    """

    praca = mommy.make('Praca')
    processo = mommy.make('ProcessoVinculacao', praca=praca)

    response = client.get(
        reverse(
            'gestor:processovinculacao-detail', kwargs={'pk': processo.pk}),
        format='json')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_returning_fields_on_a_detailed_process_not_as_owner(_common_user,
                                                             client):
    """
    Testa o retorno de informações detalhadas sobre um Processo de Vinculação,
    utilizando credenciais de identificação e não sendo dono do processo.
    """

    User = get_user_model()
    user = mommy.make(User)

    praca = mommy.make('Praca')
    processo = mommy.make('ProcessoVinculacao', praca=praca, user=user)

    response = client.get(
        reverse(
            'gestor:processovinculacao-detail', kwargs={'pk': processo.pk}),
        format='json')

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_returning_fields_on_a_detailed_process_as_owner(_common_user, client):
    """
    Testa o retorno de informações detalhadas sobre um Processo de Vinculação,
    pertencentes a um usuário.
    """

    praca = mommy.make('Praca')
    processo = mommy.make('ProcessoVinculacao', praca=praca, user=_common_user)

    fields = ('url', 'id_pub', 'praca', 'user', 'data_abertura',
              'data_finalizacao', 'aprovado', 'finalizado', 'despacho',
              'files', 'registro')

    response = client.get(
        reverse(
            'gestor:processovinculacao-detail', kwargs={'pk': processo.pk}),
        format='json')

    assert response.status_code == status.HTTP_200_OK

    for field in fields:
        assert field in response.data
        response.data.pop(field)

    assert len(response.data) == 0


def test_returning_information_about_a_Praca_on_a_detailed_process(
        _common_user, client):
    """
    Testa o retorno de informações sobre a Praça de um Processo de Vinculação
    detalhado, pertencente a um usuário.
    """

    praca = mommy.make('Praca')
    processo = mommy.make('ProcessoVinculacao', praca=praca, user=_common_user)

    fields = ('url', 'id_pub', 'nome', 'municipio', 'uf', 'modelo',
              'modelo_descricao', 'situacao', 'situacao_descricao',
              'header_img', 'gestor', 'regiao', 'repasse')

    response = client.get(
        reverse(
            'gestor:processovinculacao-detail', kwargs={'pk': processo.pk}),
        format='json')

    for field in fields:
        assert field in response.data['praca']
        response.data['praca'].pop(field)

    assert len(response.data['praca']) == 0


def test_returning_information_about_the_files_of_a_process_detailed(_common_user, client):
    """
    Testa o retorno de informações sobre os arquivos de um Processo de
    Vinculação
    """

    praca = mommy.make('Praca')
    processo = mommy.make('ProcessoVinculacao', praca=praca, user=_common_user)
    arquivos = mommy.make('ArquivosProcessoVinculacao', processo=processo,
                          _quantity=5)

    response = client.get(
        reverse(
            'gestor:processovinculacao-detail', kwargs={'pk': processo.pk}),
        format='json')

    fields = ('url', 'id_pub', 'data_envio', 'tipo', 'verificado', 'comentarios',
              'verificado_por', 'arquivo')

    for field in fields:
        assert field in response.data['files'][0]
        response.data['files'][0].pop(field)

    assert len(response.data['files'][0]) == 0


def test_upload_files_to_a_process_without_credentials(_create_temporary_file,
                                                       client):
    """
    Testa o envio de arquivos que comprovem o vinculo entre o gestor e sua
    Praça.
    """

    praca = mommy.make('Praca')
    processo = mommy.make('ProcessoVinculacao')

    test_file = _create_temporary_file
    test_file.name = 'rg-frente.jpg'

    data = {
        'tipo': 'identificação',
        'arquivo': test_file,
    }

    response = client.post(
        reverse('gestor:arquivosprocessovinculacao-list', kwargs={'processo_pk': processo.pk}),
        data,
        format='multipart')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_upload_files_to_a_process_using_diferent_credentials(
        _common_user, _create_temporary_file, client):
    """
    Testa o envio de arquivos com uma credencial diferente da utilizada para
    criar o Processo de Vinculação
    """

    User = get_user_model()

    praca = mommy.make('Praca')
    user = mommy.make(User)
    processo = mommy.make('ProcessoVinculacao', user=user)

    test_file = _create_temporary_file

    data = {
        'tipo': 'identificação',
        'arquivo': test_file,
    }

    response = client.post(
        reverse('gestor:arquivosprocessovinculacao-list', kwargs={'processo_pk': processo.pk}),
        data,
        format='multipart')

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_upload_files_to_a_process(_common_user, _create_temporary_file,
                                   client):
    """
    Testa o envio de arquivos que comprovem o vinculo entre o gestor e sua
    Praça.
    """

    praca = mommy.make('Praca')
    processo = mommy.make('ProcessoVinculacao', user=_common_user)

    test_file = _create_temporary_file
    test_file.name = 'rg-frente.jpg'

    data = {
        'tipo': 'identificação',
        'arquivo': test_file,
    }

    response = client.post(
        reverse('gestor:arquivosprocessovinculacao-list', kwargs={'processo_pk': processo.pk}),
        data,
        format='multipart')

    assert response.status_code == status.HTTP_200_OK


def test_upload_a_bunch_of_files_to_a_process(_common_user, mocker, client):
    """
    Testa o envio de varios arquivos para um Processo de Vinculação
    """

    file1 = mocker.Mock(spec=File, name='FileMock')
    file2 = mocker.Mock(spec=File, name='FileMock')
    file3 = mocker.Mock(spec=File, name='FileMock')
    file4 = mocker.Mock(spec=File, name='FileMock')

    processo = mommy.make('ProcessoVinculacao', user=_common_user)

    data = {
        'identificacao1': file1,
        'identificação2': file2,
        'identificacao3': file3,
        'identificação4': file4,
    }

    response = client.post(
        reverse('gestor:arquivosprocessovinculacao-list', kwargs={'processo_pk': processo.pk}),
        data,
        format='multipart')

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 4


def test_common_user_can_approve_process(_common_user, client):
    """
    Testa a permissão para alterar determinados campos somente com credencial
    de administrador.
    """

    processo = mommy.make('ProcessoVinculacao', user=_common_user)

    data = json.dumps({'aprovado': True})

    response = client.patch(
        reverse(
            'gestor:processovinculacao-detail', kwargs={'pk': processo.pk}),
        data,
        content_type="application/json")

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_admin_can_approve_process(_admin_user, client):
    """
    Testa a permissão para alterar determinados campos somente com credencial
    de administrador.
    """

    processo = mommy.make('ProcessoVinculacao', user=_admin_user)
    arquivos = mommy.make(
        'ArquivosProcessoVinculacao', processo=processo, verificado=True)

    data = json.dumps({'aprovado': True})

    response = client.patch(
        reverse(
            'gestor:processovinculacao-detail', kwargs={'pk': processo.pk}),
        data,
        content_type="application/json")

    assert response.status_code == status.HTTP_200_OK


def test_common_user_can_approve_process_documentation(_common_user, client):
    """
    Testa a permissão para alterar a situação da documentação de um Processo de
    Vinculação com credenciais de usuário comum.
    """

    processo = mommy.make('ProcessoVinculacao', user=_common_user)
    arquivo = mommy.make('ArquivosProcessoVinculacao', processo=processo)

    data = json.dumps({'verificado': True})

    response = client.patch(
        reverse(
            'gestor:arquivosprocessovinculacao-detail',
            kwargs={'processo_pk': processo.pk,
                    'pk': arquivo.pk}),
        data,
        content_type="application/json")

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_admin_user_can_approve_process_documentation(_admin_user, client):
    """
    Testa a permissão para alterar a situação da documentação de um Processo de
    Vinculação com credenciais de administrador.
    """

    processo = mommy.make('ProcessoVinculacao', user=_admin_user)
    arquivo = mommy.make('ArquivosProcessoVinculacao', processo=processo)

    data = json.dumps({'verificado': True})

    response = client.patch(
        reverse(
            'gestor:arquivosprocessovinculacao-detail',
            kwargs={'processo_pk': processo.pk,
                    'pk': arquivo.pk}),
        data,
        content_type="application/json")

    assert response.status_code == status.HTTP_200_OK


def test_only_approve_a_process_if_all_documentation_is_verified(_admin_user,
                                                                 client):
    """
    Testa uma situação onde um Processo de Vinculação só é aprovado se toda
    documentação estiver verificada
    """

    User = get_user_model()
    user = mommy.make(User)

    processo = mommy.make('ProcessoVinculacao', user=user)
    arquivos = mommy.make(
        'ArquivosProcessoVinculacao', processo=processo, _quantity=5)

    data = json.dumps({'aprovado': True})

    response = client.patch(
        reverse(
            'gestor:processovinculacao-detail', kwargs={'pk': processo.pk}),
        data,
        content_type="application/json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_approve_a_process_with_all_documentation_verified(_admin_user,
                                                           client):
    """
    Testa a situação onde um Processo de Vinculação é aprovado com todos os
    documentos verificados por um administrador
    """

    User = get_user_model()
    user = mommy.make(User)

    processo = mommy.make('ProcessoVinculacao', user=user)
    arquivos = mommy.make(
        'ArquivosProcessoVinculacao',
        processo=processo,
        verificado=True,
        _quantity=5)

    data = json.dumps({'aprovado': True})

    response = client.patch(
        reverse(
            'gestor:processovinculacao-detail', kwargs={'pk': processo.pk}),
        data,
        content_type="application/json")

    assert response.status_code == status.HTTP_200_OK


def test_create_a_Gestor_object_when_a_process_is_approved(_admin_user,
                                                           client):
    """
    Testa se um novo gestor é criado quando um Processo de Vinculação é
    aprovado
    """

    User = get_user_model()
    user = mommy.make(User)

    processo = mommy.make('ProcessoVinculacao', user=user)
    arquivos = mommy.make(
        'ArquivosProcessoVinculacao', processo=processo, verificado=True)

    data = json.dumps({'aprovado': True})

    response = client.patch(
        reverse(
            'gestor:processovinculacao-detail', kwargs={'pk': processo.pk}),
        data,
        content_type="application/json")

    assert response.status_code == status.HTTP_200_OK

    gestores = Gestor.objects.all()

    assert len(gestores) == 1

    assert gestores[0].praca.get_manager()


def test_only_one_manager_at_time(_admin_user, client):
    """
    Testa haver apenas um unico gesto de Praça por vez.
    """
    with pytest.raises(Exception) as e:
        User = get_user_model()
        user1 = mommy.make(User)
        user2 = mommy.make(User)

        praca = mommy.make('Praca')
        gestor = mommy.make('Gestor', praca=praca, user=user1, atual=True)
        processo = mommy.make('ProcessoVinculacao', praca=praca, user=user2)
        arquivos = mommy.make(
            'ArquivosProcessoVinculacao', processo=processo, verificado=True)

        data = json.dumps({'aprovado': True})

        response = client.patch(
            reverse(
                'gestor:processovinculacao-detail', kwargs={'pk': processo.pk}),
            data,
            content_type="application/json")

    assert str(e.value) == 'Já existe um Gestor para esta Praça'
    # assert response.status_code == status.HTTP_200_OK

    # gestores = Gestor.objects.all()
    # assert len(gestores) == 2

    # assert praca.get_manager()
    # assert len(Gestor.objects.filter(praca=praca, atual=True)) == 1


def test_return_today_date_when_create_a_new_process(client):
    """
    Testa se um processo tem instanciada a data do dia atual.
    """

    processo = mommy.make(ProcessoVinculacao)

    data = processo.data_abertura.replace(tzinfo=None)

    data_abertura = pendulum.instance(data, tz='America/Sao_Paulo')

    assert data_abertura.is_today()


def test_return_data_abertura_in_get_response(_common_user, client):
    """
    Testa o retorno da data_abertura na resposta do endpoint de Processos
    """

    processo = mommy.make(ProcessoVinculacao, user=_common_user)

    url = reverse(
        'gestor:processovinculacao-detail', kwargs={'pk': processo.pk})

    response = client.get(url)

    date = pendulum.instance(
        processo.data_abertura.replace(tzinfo=None), tz='America/Sao_Paulo')

    assert 'data_abertura' in response.data


def test_return_process_status_from_an_ente(_common_user, client):
    """
    Testa o retorno da situação do Processo de Vinculação
    """

    processo = mommy.make(ProcessoVinculacao, user=_common_user)

    response = client.get(
        reverse(
            'gestor:processovinculacao-detail', kwargs={'pk': processo.id_pub
                                                        }))

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data['aprovado'], bool)
