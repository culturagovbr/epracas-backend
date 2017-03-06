import pytest
import json
import pendulum

from django.core.files import File
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.reverse import reverse

from model_mommy import mommy

from pracas.models import Praca
from gestor.models import Gestor
from gestor.models import ProcessoVinculacao

from authentication.tests.test_user import _admin_user
from authentication.tests.test_user import _common_user

pytestmark = pytest.mark.django_db


@pytest.fixture
def _create_temporary_file(mocker):
    return mocker.Mock(spec=File, name='FileMock')


@pytest.mark.skip
def test_return_200_OK_to_Processo_list_URL(client):
    """
    Testa retorno de status 200_OK para o endpoint de Processos de Vinculação
    """

    response = client.get(
        reverse('gestor:processovinculacao-list'), format='json')
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.skip
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


@pytest.mark.skip
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


@pytest.mark.skip
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


@pytest.mark.skip
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


@pytest.mark.skip
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


@pytest.mark.skip
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


@pytest.mark.skip
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
        reverse('gestor:documento-list', kwargs={'processo_pk': processo.pk}),
        data,
        format='multipart')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.skip
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
        reverse('gestor:documento-list', kwargs={'processo_pk': processo.pk}),
        data,
        format='multipart')

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.skip
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
        reverse('gestor:documento-list', kwargs={'processo_pk': processo.pk}),
        data,
        format='multipart')

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.skip
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
        reverse('gestor:documento-list', kwargs={'processo_pk': processo.pk}),
        data,
        format='multipart')

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 4


@pytest.mark.skip
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


@pytest.mark.skip
def test_admin_can_approve_process(_admin_user, client):
    """
    Testa a permissão para alterar determinados campos somente com credencial
    de administrador.
    """

    processo = mommy.make('ProcessoVinculacao', user=_admin_user)

    data = json.dumps({'aprovado': True})

    response = client.patch(
        reverse(
            'gestor:processovinculacao-detail', kwargs={'pk': processo.pk}),
        data,
        content_type="application/json")

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.skip
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
            'gestor:documento-detail',
            kwargs={'processo_pk': processo.pk,
                    'pk': arquivo.pk}),
        data,
        content_type="application/json")

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.skip
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
            'gestor:documento-detail',
            kwargs={'processo_pk': processo.pk,
                    'pk': arquivo.pk}),
        data,
        content_type="application/json")

    assert response.status_code == status.HTTP_200_OK


def test_only_approve_an_process_if_all_documentation_is_verified(_admin_user, client):
    """
    Testa uma situação aonde um Processo de Vinculação só é aprovado se toda
    documentação estiver verificada
    """

    User = get_user_model()
    user = mommy.make(User)

    processo = mommy.make('ProcessoVinculacao', user=user)
    arquivos = mommy.make('ArquivosProcessoVinculacao', processo=processo,
                          _quantity=5) 

    data = json.dumps({'aprovado': True})

    response = client.patch(
        reverse(
            'gestor:processovinculacao-detail', kwargs={'pk': processo.pk}),
        data,
        content_type="application/json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.skip
def test_return_today_date_when_create_a_new_process(client):
    """
    Testa se um processo tem instanciada a data do dia atual.
    """

    processo = mommy.make(ProcessoVinculacao)

    data = processo.data_abertura.replace(tzinfo=None)

    data_abertura = pendulum.instance(data, tz='America/Sao_Paulo')

    assert data_abertura.is_today() == True


@pytest.mark.skip
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


@pytest.mark.skip
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
