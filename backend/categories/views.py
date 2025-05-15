from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import AllowAny

from .models import Category
from .serializers import CategorySerializer


class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.prefetch_related('subcategories').all()
    serializer_class = CategorySerializer
    permission_classes = (AllowAny,)
