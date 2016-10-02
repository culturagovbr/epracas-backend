import pytest
import json

from django.test import TestCase

from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from model_mommy import mommy

from core.models import Praca


pytestmark = pytest.mark.django_db


list_url = reverse('core:praca-list')


def test_get_URL_OK_from_Pracas(client):
    """
    Retorna 200 OK para a URL do endpoint que lista as Praças.
    """

    response = client.get(list_url, format='json')

    assert response.status_code == status.HTTP_200_OK

def test_return_a_list_of_Pracas(client):
    """
    Testa o retorno de uma lista de Praças
    """

    mommy.make_many(Praca, quantity=5)

    response = client.get(list_url, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 5
    assert isinstance(response.data, list)

def test_if_an_instance_of_list_result_has_some_properties(client):
    """
    Testa se um um dos itens(praca) de uma lista(pracas) tem
    as propriedades: url, id_pub, nome, municipio, uf, modelo,
    modelo_descricao, situacao e situacao_descricao.
    """
    fields = [
            'url',
            'id_pub',
            'nome',
            'municipio',
            'uf',
            'modelo',
            'modelo_descricao',
            'situacao',
            'situacao_descricao',
            ]

    praca = mommy.make_many(Praca, quantity=5)

    response = client.get(list_url, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 5
    for field in fields:
        assert field in response.data[0]

def test_returning_a_praca(client):
    """
    Testa o retorno de uma Praça especifica
    """

    praca = mommy.make(Praca)

    response = client.get(
        reverse('core:praca-detail', kwargs={'pk' : praca.pk}), 
        format='json'
    )
    assert response.status_code == status.HTTP_200_OK
    assert str(praca.pk) in response.data['id_pub']

def test_return_a_praca_with_some_properties(client):
    """
    Testa o retorno de uma praça especifica com as seguintes propriedades:
    url, id_pub, nome, slug, municipio, uf, modelo, modelo_descricao, situacao e
    situacao_descricao.

    """

    fields = [
            'url',
            'id_pub',
            'nome',
            'slug',
            'municipio',
            'uf',
            'modelo',
            'modelo_descricao',
            'situacao',
            'situacao_descricao',
            ]

    praca = mommy.make(Praca)

    response = client.get(
            reverse('core:praca-detail', kwargs={'pk': praca.pk}),
            format='json'
            )

    assert response.status_code == status.HTTP_200_OK
    for field in fields:
        assert field in response.data

def test_not_returning_a_praca_giving_wrong_args(client):

    mommy.make(Praca)

    response = client.get(
            reverse('core:praca-detail', kwargs={'pk': 1}),
            format='json'
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_create_a_new_praca(client):

    praca = {
            'nome': 'Praça Fulano Cicrano',
            'contrato': '36338510',
            'regiao': 'n',
            'uf': 'AM',
            'municipio': 'Manaus',
            'modelo': 'g',
            'situacao': 'i'
            }

    response = client.post(
            reverse('core:praca-list'),
            praca,
            format='json'
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert '36338510' in bytes.decode(response.content)
    assert Praca.objects.count() == 1

def test_retorna_as_5_pracas_mais_proximas(client):

    data = {
            'lat': -15.7833,
            'long':  -47.9167
    }

    for i in range(10):
        praca = mommy.make(Praca, _fill_optional=['lat', 'long'])


    response = client.post(
            reverse('core:distancia'),
            data,
            format='json'
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 5
    assert sorted(response.data, key=lambda praca: praca['distancia']) == response.data

def test_defining_a_name_if_user_leave_it_blank(client):
    """
    Testa a situação onde um usuário deixa o nome da Praça em branco
    e o sistema define o nome da praça como CEU + Nome da Cidade e UF

    """

    praca = mommy.make(Praca, nome="", municipio="Brasilia", uf="DF")

    response = client.get(
            reverse('core:praca-detail', kwargs={'pk': praca.id_pub}),
            format='json'
            )

    assert response.status_code == status.HTTP_200_OK
    assert response.data['nome'] == "CEU de Brasilia - DF"

def test_defining_a_slug_from_the_name(client):
    """
    Testa a construção automática de um slug a partir do nome da Praça
    """

    from django.utils.text import slugify

    praca = mommy.make(Praca, nome="Praça Fulano Cicrano")

    slug = slugify(praca.nome)

    response = client.get(
            reverse('core:praca-detail', kwargs={'pk': praca.id_pub}),
            format='json'
            )

    assert response.status_code == status.HTTP_200_OK
    assert response.data['slug'] == slug

def test_defining_a_name_and_a_slug(client):
    """
    Testa a definição automatica de um nome de Praça e uma slug, a partir
    do nome do municipio e da UF.
    """

    from django.utils.text import slugify

    praca = mommy.make(Praca, nome="")

    slug = slugify(praca.nome)

    response = client.get(
            reverse('core:praca-detail', kwargs={'pk': praca.id_pub}),
            format='json'
            )

    assert response.status_code == status.HTTP_200_OK
    assert response.data['slug'] == slug

def test_returning_an_image_for_header(client):
    """
    Testa o retorno de um parametro com uma URL de uma imagem do cabeçalho
    para a pagina de uma Praça.
    """

    praca = mommy.make(Praca)

    response = client.get(
            reverse('core:praca-detail', kwargs={'pk': praca.id_pub}),
            format='json'
            )

    assert response.status_code == status.HTTP_200_OK
    assert 'header_img' in response.data


