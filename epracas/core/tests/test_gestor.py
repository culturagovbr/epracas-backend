import pytest

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
