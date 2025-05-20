import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from io import BytesIO
from PIL import Image

from categories.models import Category, SubCategory
from products.models import Product

pytestmark = pytest.mark.django_db


def get_fake_image_file(
        filename='test.jpg', size=(100, 100), color=(255, 0, 0)
):
    file = BytesIO()
    image = Image.new("RGB", size=size, color=color)
    image.save(file, 'JPEG')
    file.seek(0)
    return SimpleUploadedFile(
        name=filename, content=file.read(), content_type='image/jpeg'
    )


def test_get_products_returns_200_and_data():
    client = APIClient()

    # Создаем тестовую категорию и подкатегорию
    category = Category.objects.create(
        name='Фрукты', slug='fruits', image='cat.jpg'
    )
    subcategory = SubCategory.objects.create(
        name='Цитрусовые', slug='citrus', image='sub.jpg', category=category
    )

    # Создаем продукт
    Product.objects.create(
        name='Апельсин',
        slug='orange',
        description='Апельсин',
        price=99.90,
        image=get_fake_image_file(),
        category=category,
        subcategory=subcategory
    )

    url = reverse('products-list')
    response = client.get(url)

    assert response.status_code == 200
    assert response.data['results'][0]['name'] == 'Апельсин'
    assert 'images' in response.data['results'][0]
    assert len(response.data['results'][0]['images']) == 3
