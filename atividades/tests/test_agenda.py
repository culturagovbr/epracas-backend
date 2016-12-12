import json
import pytest

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from model_mommy import mommy

from authentication.tests.test_user import authentication

pytestmark = pytest.mark.django_db

agenda_list_url = reverse('atividades:agenda-list')


def test_return_200_OK_on_main_endpoint_url(client):

    response = client.get(agenda_list_url)

    assert response.status_code == status.HTTP_200_OK


def test_return_a_list_with_5_events(client):

    mommy.make_many('Agenda', quantity=5)

    response = client.get(agenda_list_url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 5


def test_return_event_properties(client):
    """
    Testa o retorno de determinadas propriedades de um Evento,
    que são: url, id_pub, praca_url, praca_id_pub, titulo, data_inicio,
    data_encerramento, horario_inicio, horario_encerramento, descricao e
    local.
    """

    fields = [
            'url',
            'id_pub',
            'praca_url',
            'praca',
            'titulo',
            'descricao',
            'justificativa',
            'tipo',
            'area',
            'espaco',
            # 'parceiros',
            'faixa_etaria',
            'publico_participante',
            'abrangencia_territorial',
            'data_inicio',
            'data_encerramento',
            'periodicidade',
            'hora_inicio',
            'hora_encerramento',
            'carga_horaria',
            'publico_esperado',
    ]

    praca = mommy.make('Praca')
    evento = mommy.make('Agenda', praca=praca)

    response = client.get(
            reverse('atividades:agenda-detail', kwargs={'pk': evento.id_pub})
            )

    assert response.status_code == status.HTTP_200_OK
    for field in fields:
        assert field in response.data


def test_return_events_related_with_a_Praca(client):

    praca = mommy.make('Praca')
    mommy.make('Agenda', praca=praca)

    response = client.get(
            reverse('pracas:praca-detail', kwargs={'pk': praca.id_pub})
            )

    assert response.status_code == status.HTTP_200_OK
    assert 'agenda' in response.data


def test_closing_an_event_occurrence(authentication):

    client = APIClient()

    praca = mommy.make('Praca')
    ocorrencia = mommy.make('Agenda', praca=praca)

    request_data = {
        "relatorio": {
            "realizado": "true",
            "publico_presente": "100",
            "pontos_positivos": "Pontos Positivos",
            "pontos_negativos": "Pontos negativos",
        },
    }

    response = client.patch(
        reverse('atividades:agenda-detail', kwargs={'pk': ocorrencia.id_pub}),
        request_data,
        # content_type='application/json',
        format='json'
        )

    assert response.status_code == status.HTTP_200_OK

    response = client.get(
        reverse('atividades:agenda-detail', kwargs={'pk': ocorrencia.id_pub}),
        format='json',
        )

    # import ipdb
    # ipdb.set_trace()
    assert response.status_code == status.HTTP_200_OK
    assert json.dumps(request_data) in str(response.content)
