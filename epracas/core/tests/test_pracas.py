import pytest
import json

from django.test import TestCase

from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from model_mommy import mommy

from core.models import Praca


@pytest.mark.django_db
class PracaTest(APITestCase):

    def setUp(self):

        self.list_url = reverse('core:praca-list')
        self.data = {
            'contrato': '1111111111',
            'regiao': 'co',
            'uf': 'df',
            'municipio': 'Brasilia',
            'modelo': 'g',
            'situacao': 'i'
            }

    def test_get_URL_OK_from_Pracas(self):

        response = self.client.get(self.list_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_return_a_list_of_Pracas(self):

        praca = Praca()
        praca.contrato = '1'*10
        praca.regiao = 'co' 
        praca.UF = 'DF'
        praca.municipio = 'Brasilia'
        praca.modelo = 'g'
        praca.situacao = 'i'
        praca.save()

        response = self.client.get(self.list_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertIsInstance(response.data, list)

    def test_returning_a_praca(self):

        data = self.data

        praca = Praca()
        praca.contrato = data['contrato']
        praca.regiao = data['regiao']
        praca.UF = data['uf']
        praca.municipio = data['municipio']
        praca.modelo = data['modelo']
        praca.situacao = data['situacao']
        praca.save()

        response = self.client.get(
            reverse('core:praca-detail', kwargs={'pk' : praca.pk}), 
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(
                response,
                praca.pk,
                status_code=status.HTTP_200_OK
        )

    def test_not_returning_a_praca_giving_wrong_args(self):

        data = self.data

        praca = Praca()
        praca.contrato = data['contrato']
        praca.regiao = data['regiao']
        praca.UF = data['uf']
        praca.municipio = data['municipio']
        praca.modelo = data['modelo']
        praca.situacao = data['situacao']
        praca.save()

        response = self.client.get(
                reverse('core:praca-detail', kwargs={'pk': 1}),
                format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

@pytest.mark.django_db
def test_create_a_new_praca(client):
    praca = {
            'contrato': '36338510',
            'regiao': 'n',
            'uf': 'PA',
            'municipio': 'Abaetetuba',
            'modelo': 'm',
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

@pytest.mark.django_db
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
