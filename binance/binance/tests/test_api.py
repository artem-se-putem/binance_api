from django.urls import reverse
from rest_framework import status
import pytest

@pytest.mark.django_db
def test_get_crypto_list(api_client):
    url = reverse('crypto-list')
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK