from django.test import TestCase

from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.test import APITestCase


class PracaTest(APITestCase):

    def setUp(self):

        self.url = reverse('core:praca-list')

    def test_get_URL_OK_from_Pracas(self):

        response = self.client.get(self.url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
