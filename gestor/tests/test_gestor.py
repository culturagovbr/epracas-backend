import pytest
import json

from rest_framework import status
from rest_framework.reverse import reverse

from model_mommy import mommy

from gestor.models import Gestor

pytestmark = pytest.mark.django_db


@pytest.mark.skip
def test_return_200_ok_gestor_endpoint(client):
    """
    Testa retorno 200 OK do endpoint dos Gestores
    """

    response = client.get(reverse('gestor:gestor-list'))
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.skip
def test_persist_a_gestor_name_without_credentials(client):
    """
    Testa a persistencia de um Gestor sem credenciais de identificação
    """

    gestor = {
            'nome': 'Fulano Cicrano'
    }

    response = client.post(
            reverse('gestor:gestor-list'),
            gestor,
            format='json'
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.skip
def test_return_an_id_pub_for_a_created_gestor(client):
    """
    Testa o retorno do identificador publico(id_pub) de um determinado gestor.
    """

    gestor = {
            'nome': 'Fulano Cicrano'
    }

    response = client.post(
            reverse('gestor:gestor-list'),
            gestor,
            format='json'
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert 'id_pub' in bytes.decode(response.content)


@pytest.mark.skip
def test_return_a_created_gestor(client):
    """
    Testa o retorno de um gestor recem criado.
    """

    gestor = {
            'nome': 'Fulano Cicrano'
    }

    post = client.post(
            reverse('gestor:gestor-list'),
            gestor,
            format='json'
    )
    assert post.status_code == status.HTTP_201_CREATED

    id_pub = json.loads(bytes.decode(post.content))['id_pub']

    response = client.get(
            reverse('gestor:gestor-detail', kwargs={'pk': id_pub}),
            format='json'
            )
    assert response.status_code == status.HTTP_200_OK
    assert gestor['nome'] in bytes.decode(response.content)


@pytest.mark.skip
def test_persist_a_gestors_address(client):
    """
    Testa persistir o endereço de um gestor
    """

    gestor = {
            'nome': 'Fulano Cicrano',
            'endereco': 'Conj 10, Casa 19',
            'cidade': 'Altamira',
            'uf': 'pa',
            'regiao': 'N'
    }

    response = client.post(
            reverse('gestor:gestor-list'),
            gestor,
            format='json'
    )
    response_content = json.loads(bytes.decode(response.content))
    response_content.pop('id_pub')

    assert response.status_code == status.HTTP_201_CREATED

    assert gestor == response_content


@pytest.mark.skip
def test_update_a_gestors_address(client):
    """
    Testa atulizar o endereço de um gestor
    """

    gestor = {
            'nome': 'Fulano Cicrano',
            'endereco': 'Conj 10, Casa 19',
            'cidade': 'Altamira',
            'uf': 'pa',
            'regiao': 'N'
    }

    post = client.post(
            reverse('gestor:gestor-list'),
            gestor,
            format='json'
    )
    assert post.status_code == status.HTTP_201_CREATED

    id_pub = json.loads(bytes.decode(post.content)).pop('id_pub')

    update = client.put(
            reverse('gestor:gestor-detail', kwargs={'pk': id_pub}),
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


@pytest.mark.skip
def test_return_a_FQDN_URL_from_Gestor_method(client):
    """
    Testa retornar uma URL a partir de um metodo da classe Gestor.
    """

    gestor = mommy.make(Gestor, nome='Fulano Cicrano')
    url = reverse(
            'gestor:gestor-detail',
            kwargs={'pk': gestor.id_pub},
          )
    response = client.get(url, format='json')
    gestor_url = gestor.get_absolute_url()

    assert response.status_code == status.HTTP_200_OK
    assert gestor_url == url
