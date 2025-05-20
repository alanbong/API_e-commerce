from rest_framework import serializers

from products.models import Product
from products.serializers import ProductSerializer
from .models import Cart, CartItem
from .constants import MAX_PRODUCT_QUANTITY_VALUE


class CartItemSerializer(serializers.ModelSerializer):
    '''
    Вложенный сериалзиатор для CartSerializer.
    '''
    product = ProductSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ('product', 'quantity', 'total_price')

    def get_total_price(self, obj):
        return obj.product.price * obj.quantity


class CartSerializer(serializers.ModelSerializer):
    '''
    Сериализатор корзины с подсчётом общей суммы и количества.
    '''
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ('items', 'total_price')

    def get_total_price(self, obj):
        return sum(item.product.price * item.quantity for item in obj.items.all())


class CartItemActionSerializer(serializers.Serializer):
    '''
    Сериализатор товаров в коризине для операций:
    добавления/изменения/удаления товара.
    '''
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )
    quantity = serializers.IntegerField(
        min_value=1,
        max_value=MAX_PRODUCT_QUANTITY_VALUE,
        required=False,
        error_messages={
            'min_value': 'Минимальное количество единиц товара - 1',
            'max_value': 'Максимальное количество единиц товара - 9999',
        }
    )

    class Meta:
        fields = ('product_id', 'quantity')
