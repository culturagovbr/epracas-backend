import pytest

from rest_framework import status
from rest_framework.reverse import reverse


@pytest.mark.django_db
def test_return_200_OK_to_Processo_list_URL(client):
    """TODO: Docstring for test_return_200_OK_to_Processo_list_URL(client.
    :returns: TODO

    """

    response = client.get(
            reverse('core:processoadmissao-list'),
            format='json'
    )
    assert response.status_code == status.HTTP_200_OK
