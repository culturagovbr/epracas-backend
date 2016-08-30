import pytest
import json

from rest_framework import status
from rest_framework.reverse import reverse

from model_mommy import mommy

from core.models import Gestor, ProcessoAdmissao


@pytest.mark.django_db
def test_return_200_OK_to_Processo_list_URL(client):
    """TODO: Docstring for test_return_200_OK_to_Processo_list_URL(client.
    :returns: TODO

    """

    response = client.get(
            reverse('core:processoadmissao-list'),
            format='json'
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_persist_a_process_using_POST(client):
    """TODO: Docstring for test_list_all_process(client.
    :returns: TODO

    """

    gestor = mommy.make(Gestor, nome = "Fulano Cicrano")

    data = {
            'gestor': gestor.id_pub
    }

    post = client.post(
            reverse('core:processoadmissao-list'),
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
    import pendulum
    import datetime

    gestor = mommy.make(Gestor, nome="Fulano Cicrano")
    processo = mommy.make(ProcessoAdmissao, gestor=gestor)

    data = processo.data_abertura.replace(tzinfo=None)

    data_abertura = pendulum.instance(
            data,
            tz='America/Sao_Paulo'
    )

    assert data_abertura.is_today() == True
