import pytest
import json

from rest_framework import status
from rest_framework.reverse import reverse

from model_mommy import mommy

pytestmark = pytest.mark.django_db


def test_return_200_ok_gestor_endpoint(client):
    """
    Testa retorno 200 OK do endpoint dos Gestores
    """

    response = client.get(reverse('gestor:gestor-list'))
    assert response.status_code == status.HTTP_200_OK


def test_return_manager_data_from_endpoint(client):
    """
    Testa o retorno de informações sobre um gestor de uma Praça
    """

    gestor = mommy.make('Gestor')

    response = client.get(reverse('gestor:gestor-detail', kwargs={'pk': gestor.pk}))

    assert response.status_code == status.HTTP_200_OK
    assert 'url' in response.data
    assert 'nome' in response.data
    assert 'email' in response.data


def test_return_a_praca_with_manager_information(client):
    """
    Testa o retorno de uma Praça com a informação do seu atual gestor
    """

    gestor = mommy.make('Gestor')

    response = client.get(reverse('pracas:praca-detail', kwargs={'pk':
                                                                 gestor.praca.pk}))

    assert response.status_code == status.HTTP_200_OK
    assert 'gestor' in response.data
    assert 'nome' in response.data['gestor']


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
