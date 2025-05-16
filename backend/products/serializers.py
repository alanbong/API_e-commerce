from rest_framework import serializers

from typing import List, Dict, Optional

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Category.
    """
    category = serializers.StringRelatedField(read_only=True)
    subcategory = serializers.StringRelatedField(read_only=True)

    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'slug',
            'description',
            'price',
            'images',
            'subcategory',
            'category',
        )
        read_only_fields = ('category',)

    def get_images(self, obj) -> List[Dict[str, Optional[str]]]:
        """
        Возвращает список изображений с размерами и URL.
        """
        sizes = ['small', 'medium', 'large']
        fields = [obj.image_small, obj.image_medium, obj.image_large]

        return [
            {'size': size, 'url': image.url if image else None}
            for size, image in zip(sizes, fields)
        ]
