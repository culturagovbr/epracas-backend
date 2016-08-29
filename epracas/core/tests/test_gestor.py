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


@pytest.mark.django_db
def test_return_a_created_gestor(client):
    """TODO: Docstring for test_return_a_created_gestor(client.
    :returns: TODO

    """

    gestor = {
            'nome': 'Fulano Cicrano'
    }

    post = client.post(
            reverse('core:gestor-list'),
            gestor,
            format='json'
    )
    assert post.status_code == status.HTTP_201_CREATED

    id_pub = json.loads(bytes.decode(post.content))['id_pub']

    response = client.get(
            reverse('core:gestor-detail', kwargs={'pk': id_pub}),
            format='json'
            )
    assert response.status_code == status.HTTP_200_OK
    assert gestor['nome'] in bytes.decode(response.content)


@pytest.mark.django_db
def test_persist_a_gestors_address(client):
    """TODO: Docstring for test_persist_a_gestors_address.
    :returns: TODO

    """
    gestor = {
            'nome': 'Fulano Cicrano',
            'endereco': 'Conj 10, Casa 19',
            'cidade': 'Altamira',
            'uf': 'PA',
            'regiao': 'n'
    }

    response = client.post(
            reverse('core:gestor-list'),
            gestor,
            format='json'
    )
    response_content = json.loads(bytes.decode(response.content))
    response_content.pop('id_pub')

    assert response.status_code == status.HTTP_201_CREATED

    assert gestor == response_content


@pytest.mark.django_db
def test_update_a_gestors_address(client):
    """TODO: Docstring for test_update_a_gestors_address.

    :returns: TODO

    """

    gestor = {
            'nome': 'Fulano Cicrano',
            'endereco': 'Conj 10, Casa 19',
            'cidade': 'Altamira',
            'uf': 'PA',
            'regiao': 'n'
    }

    post = client.post(
            reverse('core:gestor-list'),
            gestor,
            format='json'
    )
    assert post.status_code == status.HTTP_201_CREATED

    id_pub = json.loads(bytes.decode(post.content)).pop('id_pub')

    update = client.put(
            reverse('core:gestor-detail', kwargs={'pk': id_pub}),
            json.dumps({
                'nome': 'Fulano Cicrano',
                'endereco': 'Conj 11, Casa 20'
            }),
            format='json',
            content_type='application/json'
    )
    update_content = bytes.decode(update.content)

    assert update.status_code == status.HTTP_200_OK
    assert 'Conj 11, Casa 20' in update_content
