import pytest

from django.contrib.auth import get_user_model

from rest_framework import status

from core.helper_functions import _

from model_mommy import mommy


User = get_user_model()
pytestmark = pytest.mark.django_db

_list = _('pracas:rh-list')
_detail = _('pracas:rh-detail')


def test_get_URL_OK_from_RH_endpoint(client):
    """
    Testa retornar 200 OK para a URL do endpoint que lista todos os Recursos
    Humanos de uma Praça
    """

    praca = mommy.make('Praca')

    response = client.get(_list(kwargs={'praca_pk': praca.pk}),
                          content_type='application/json')

    assert response.status_code == status.HTTP_200_OK
