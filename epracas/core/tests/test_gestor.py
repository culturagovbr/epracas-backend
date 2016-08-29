import pytest
import json

from rest_framework import status
from rest_framework.reverse import reverse

from core.models import Gestor


@pytest.mark.django_db
def test_return_200_ok_gestor_endpoint(client):
    """TODO: Docstring for test_return_200_ok_gestor_endpoint.
    :returns: TODO

    """

    response = client.get(reverse('core:gestor-list'))
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_persist_a_gestor_name(client):
    """TODO: Docstring for test_return_a_gestor_list(client.
    :returns: TODO

    """

    gestor = {
            'nome': 'Fulano Cicrano'
    }

    response = client.post(
            reverse('core:gestor-list'),
            gestor,
            format='json'
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert gestor['nome'] in bytes.decode(response.content)


@pytest.mark.django_db
def test_return_an_id_pub_for_a_created_gestor(client):
    """TODO: Docstring for test_return_an_id_pub_for_a_created_gestor.

    :arg1: TODO
    :returns: TODO

    """

    gestor = {
            'nome': 'Fulano Cicrano'
    }

    response = client.post(
            reverse('core:gestor-list'),
            gestor,
            format='json'
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert 'id_pub' in bytes.decode(response.content)
