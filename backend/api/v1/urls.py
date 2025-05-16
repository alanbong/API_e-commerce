from django.urls import path, include
from rest_framework.routers import DefaultRouter

from categories.views import CategoryViewSet
from products.views import ProductViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('products', ProductViewSet, basename='products')

urlpatterns = [
    path('', include(router.urls)),
]
