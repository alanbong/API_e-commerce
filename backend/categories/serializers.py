from rest_framework import serializers

from .models import Category, SubCategory


class SubCategorySerializer(serializers.ModelSerializer):
    """Сериализатор Модели SubCategory."""
    class Meta:
        model = SubCategory
        fields = ('id', 'name', 'slug', 'image')


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'image', 'subcategories')
