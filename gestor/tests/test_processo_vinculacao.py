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


def test_upload_a_bunch_of_files_to_a_process(_common_user, mocker, client):

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


def test_return_today_date_when_create_a_new_process(client):
    """
    Testa se um processo tem instanciada a data do dia atual.
    """

    processo = mommy.make(ProcessoVinculacao)

    data = processo.data_abertura.replace(tzinfo=None)

    data_abertura = pendulum.instance(data, tz='America/Sao_Paulo')

    assert data_abertura.is_today() == True


@pytest.mark.skip
def test_return_data_abertura_in_get_response(client):
    """TODO: Docstring for test_return_data_abertura_in_get_response.
    :returns: TODO

    """
    gestor = mommy.make(Gestor, nome="Fulano Cicrano")
    processo = mommy.make(ProcessoVinculacao, gestor=gestor)

    url = reverse('gestor:processovinculacao-list') + '?gestor={}'.format(
        gestor.id_pub)

    response = client.get(url)

    date = pendulum.instance(
        processo.data_abertura.replace(tzinfo=None), tz='America/Sao_Paulo')

    response_data = bytes.decode(response.content)
    dict_data = json.loads(response_data)[0]

    assert 'data_abertura' in dict_data


@pytest.mark.skip
def test_return_process_status_from_an_ente(client):
    """TODO: Docstring for test_return_process_status_from_an_ente.
    :returns: TODO

    """

    gestor = mommy.make(Gestor, nome="Fulano Cicrano")
    processo = mommy.make(ProcessoVinculacao, gestor=gestor)

    url = reverse(
        'gestor:processovinculacao-detail',
        kwargs={'pk': processo.id_pub}, )

    response = client.get(url)
    response_aprovado = response.data['aprovado']

    assert isinstance(processo.aprovado, bool) == True
    assert response_aprovado == processo.aprovado
