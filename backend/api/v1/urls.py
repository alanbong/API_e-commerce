from django.urls import path, include
from rest_framework.routers import DefaultRouter

from categories.views import CategoryViewSet
from products.views import ProductViewSet
from cart.views import CartViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('products', ProductViewSet, basename='products')
router.register(r'cart', CartViewSet, basename='cart')

urlpatterns = [
    path('', include(router.urls)),
]
