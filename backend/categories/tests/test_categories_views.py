import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from categories.models import Category

pytestmark = pytest.mark.django_db


def test_get_categories_returns_200_and_data():
    client = APIClient()

    # Создаём категорию
    Category.objects.create(
        name='Молочные продукты',
        slug='dairy',
        image='test.jpg'
    )

    url = reverse('category-list')
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert any(
        cat['name'] == 'Молочные продукты' for cat in response.data['results']
    )
