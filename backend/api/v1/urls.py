from django.urls import path, include
from django.views.static import serve
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from shop_backend.settings import BASE_DIR

from categories.views import CategoryViewSet
from products.views import ProductViewSet
from cart.views import CartViewSet


DOCS_DIR = BASE_DIR / 'utils'

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('products', ProductViewSet, basename='products')
router.register(r'cart', CartViewSet, basename='cart')


urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path(
        'redoc/', serve,
        {'path': 'redoc.html', 'document_root': DOCS_DIR},
        name='redoc'
    ),
    path(
        'redoc/openapi-schema.yml/', serve,
        {'path': 'openapi-schema.yml', 'document_root': DOCS_DIR},
        name='schema-yaml'
    ),
    path('swagger/', serve, {
        'path': 'swagger.html',
        'document_root': DOCS_DIR
    }, name='swagger-ui'),
    path(
        'swagger/openapi-schema.yml/', serve,
        {'path': 'openapi-schema.yml', 'document_root': DOCS_DIR},
        name='schema-yaml'
    ),
]
