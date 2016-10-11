import pytest
import json
import pendulum
import datetime

from rest_framework import status
from rest_framework.reverse import reverse

from model_mommy import mommy

from core.models import Praca, Gestor, ProcessoVinculacao


@pytest.mark.django_db
def test_return_200_OK_to_Processo_list_URL(client):
    """TODO: Docstring for test_return_200_OK_to_Processo_list_URL(client.
    :returns: TODO

    """

    response = client.get(
            reverse('core:processovinculacao-list'),
            format='json'
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_persist_a_process_using_POST(client):
    """TODO: Docstring for test_list_all_process(client.
    :returns: TODO

    """

    gestor = mommy.make(Gestor, nome = "Fulano Cicrano")
    praca = mommy.make(Praca)

    data = {
            'gestor': gestor.id_pub,
            'praca': praca.id_pub,
    }

    post = client.post(
            reverse('core:processovinculacao-list'),
            data,
            format='json'
    )

    post_content = bytes.decode(post.content)
    id_pub_gestor = json.loads(post_content).pop('gestor')

    assert post.status_code == status.HTTP_201_CREATED
    assert str(id_pub_gestor) in str(gestor.id_pub)


@pytest.mark.django_db
def test_return_today_date_when_create_a_new_process(client):
    """TODO: Docstring for test_return_today_date_when_create_a_new_process.
    :returns: TODO

    """

    gestor = mommy.make(Gestor, nome="Fulano Cicrano")
    processo = mommy.make(ProcessoVinculacao, gestor=gestor)

    data = processo.data_abertura.replace(tzinfo=None)

    data_abertura = pendulum.instance(
            data,
            tz='America/Sao_Paulo'
    )

    assert data_abertura.is_today() == True


@pytest.mark.django_db
def test_return_data_abertura_in_get_response(client):
    """TODO: Docstring for test_return_data_abertura_in_get_response.
    :returns: TODO

    """
    gestor = mommy.make(Gestor, nome="Fulano Cicrano")
    processo = mommy.make(ProcessoVinculacao, gestor=gestor)

    url = reverse('core:processovinculacao-list') + '?gestor={}'.format(gestor.id_pub)

    response = client.get(url)

    date = pendulum.instance(
        processo.data_abertura.replace(tzinfo=None),
        tz='America/Sao_Paulo'
        )

    response_data = bytes.decode(response.content)
    dict_data = json.loads(response_data)[0]

    assert 'data_abertura' in dict_data


@pytest.mark.django_db
def test_return_process_status_from_an_ente(client):
    """TODO: Docstring for test_return_process_status_from_an_ente.
    :returns: TODO

    """

    gestor = mommy.make(Gestor, nome="Fulano Cicrano")
    processo = mommy.make(ProcessoVinculacao, gestor=gestor)

    url = reverse(
            'core:processovinculacao-detail',
            kwargs={'pk': processo.id_pub},
            )

    response = client.get(url)
    response_aprovado = response.data['aprovado']

    assert isinstance(processo.aprovado, bool) == True
    assert response_aprovado == processo.aprovado
