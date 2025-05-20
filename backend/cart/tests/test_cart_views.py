import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from PIL import Image

from categories.models import Category, SubCategory
from products.models import Product

pytestmark = pytest.mark.django_db
User = get_user_model()


@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='test')


@pytest.fixture
def auth_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def test_image():
    file = BytesIO()
    image = Image.new("RGB", (100, 100), color=(255, 0, 0))
    image.save(file, 'JPEG')
    file.seek(0)
    return SimpleUploadedFile('test.jpg', file.read(), content_type='image/jpeg')


@pytest.fixture
def orange_product(test_image):
    category = Category.objects.create(name='Фрукты', slug='fruits', image=test_image)
    subcategory = SubCategory.objects.create(name='Цитрусовые', slug='citrus', image=test_image, category=category)
    return Product.objects.create(
        name='Апельсин',
        slug='orange',
        description='Апельсин',
        price=99.90,
        image=test_image,
        category=category,
        subcategory=subcategory
    )


@pytest.fixture
def cart_urls():
    return {
        'list': reverse('cart-list'),
        'add': reverse('cart-add-product'),
        'update': reverse('cart-update-product'),
        'remove': reverse('cart-remove-product'),
        'clear': reverse('cart-clear-cart'),
    }


@pytest.fixture
def cart_with_product(auth_client, orange_product, cart_urls):
    auth_client.post(cart_urls['add'], {'product_id': orange_product.id, 'quantity': 1}, format='json')
    return auth_client, orange_product


def test_cart_requires_authentication():
    client = APIClient()
    url = reverse('cart-list')
    response = client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_add_product_to_cart(auth_client, orange_product, cart_urls):
    auth_client.post(cart_urls['add'], {'product_id': orange_product.id, 'quantity': 2}, format='json')

    response = auth_client.get(cart_urls['list'])
    items = response.data['items']

    assert response.status_code == 200
    assert len(items) == 1
    assert items[0]['product']['name'] == 'Апельсин'
    assert items[0]['quantity'] == 2


def test_update_quantity(cart_with_product, cart_urls):
    client, orange = cart_with_product
    client.patch(cart_urls['update'], {'product_id': orange.id, 'quantity': 5}, format='json')

    response = client.get(cart_urls['list'])
    assert response.data['items'][0]['quantity'] == 5


def test_remove_product(cart_with_product, cart_urls):
    client, orange = cart_with_product
    client.delete(cart_urls['remove'], {'product_id': orange.id}, format='json')

    response = client.get(cart_urls['list'])
    assert response.data['items'] == []


def test_clear_cart(cart_with_product, cart_urls):
    client, _ = cart_with_product
    client.delete(cart_urls['clear'])

    response = client.get(cart_urls['list'])
    assert response.data['items'] == []
