from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import AllowAny

from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(ReadOnlyModelViewSet):
    """
    Представление для модели Product.
    """
    queryset = Product.objects.select_related('category', 'subcategory').all()
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)
