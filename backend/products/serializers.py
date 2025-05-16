from rest_framework import serializers

from categories.models import SubCategory
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""
    category = serializers.StringRelatedField(read_only=True)
    subcategory = serializers.PrimaryKeyRelatedField(
        queryset=SubCategory.objects.all()
    )

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'slug',
            'description',
            'price',
            'image',
            'subcategory',
            'category',
        )
        read_only_fields = ('category',)
