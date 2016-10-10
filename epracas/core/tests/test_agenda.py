import pytest

from rest_framework import status
from rest_framework.reverse import reverse

from model_mommy import mommy


pytestmark = pytest.mark.django_db

agenda_list_url = reverse('core:agenda-list')

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
            'data_inicio',
            'data_encerramento',
            'hora_inicio',
            'hora_encerramento',
            'descricao',
            'local',
    ]

    praca = mommy.make('Praca')
    evento = mommy.make('Agenda', praca=praca)

    response = client.get(
            reverse('core:agenda-detail', kwargs={'pk': evento.id_pub})
            )

    assert response.status_code == status.HTTP_200_OK
    for field in fields:
        assert field in response.data


def test_return_events_related_with_a_Praca(client):

	praca = mommy.make('Praca')
	evento = mommy.make('Agenda', praca=praca)

	response = client.get(
			reverse('core:praca-detail', kwargs={'pk': praca.id_pub})
			)

	assert response.status_code == status.HTTP_200_OK
	assert 'agenda' in response.data
