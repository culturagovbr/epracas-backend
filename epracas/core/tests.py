import json

from collections import OrderedDict

from django.test import TestCase

from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Praca


class PracaTest(APITestCase):

    def setUp(self):

        self.url = reverse('core:praca-list')

    def test_get_URL_OK_from_Pracas(self):

        response = self.client.get(self.url, format='json')

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

        response = self.client.get(self.url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertIsInstance(response.data, list)
