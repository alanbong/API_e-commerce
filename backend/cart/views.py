from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemActionSerializer


class CartViewSet(viewsets.ModelViewSet):
    '''
    Viewset для работы с коризной.
    Просмотр, добавление, изменение, удаление товаров.
    '''
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        '''
        Выбор сериализатора в зависимости от действия.
        '''
        if self.action in ('add_product', 'update_product', 'remove_product'):
            return CartItemActionSerializer
        return CartSerializer

    def get_queryset(self):
        '''
        Только корзина текущего пользователя.
        '''
        return Cart.objects.filter(user=self.request.user)

    def get_object(self):
        '''
        Получаем или создаем корзину при первом обращении.
        '''
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart

    def list(self, request, *args, **kwargs):
        '''
        Переопределяем GET /cart/ для получения 1 объекта.
        '''
        cart = self.get_object()
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    def _get_cart_and_product(self, request):
        '''
        Общий метод извлечения валидировнных данных для
        add_product, update_product, remove_product.
        '''
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.validated_data['product']
        quantity = serializer.validated_data.get('quantity')
        cart = self.get_object()
        return cart, product, quantity

    @action(detail=False, methods=('post',), url_path='add')
    def add_product(self, request):
        cart, product, quantity = self._get_cart_and_product(request)
        if quantity is None:
            quantity = 1

        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        item.quantity = item.quantity + quantity if not created else quantity
        item.save()

        return Response({'status': 'added'})

    @action(detail=False, methods=('patch',), url_path='update')
    def update_product(self, request):
        cart, product, quantity = self._get_cart_and_product(request)
        if quantity is None:
            return Response(
                {'error': (
                    'Параметр количества продуктов '
                    '"quantity" обазятелен'
                )}, status=status.HTTP_400_BAD_REQUEST
            )

        item = get_object_or_404(CartItem, cart=cart, product=product)
        item.quantity = quantity
        item.save()
        return Response({'status': 'Корзина обновлена'})

    @action(detail=False, methods=('delete',), url_path='remove')
    def remove_product(self, request):
        cart, product, _ = self._get_cart_and_product(request)

        deleted_count, _ = CartItem.objects.filter(
            cart=cart, product=product
        ).delete()

        if not deleted_count:
            return Response(
                {'error': 'Продукт не найден в корзине'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=('delete',), url_path='clear')
    def clear_cart(self, request):
        cart = self.get_object()
        cart.items.all().delete()
        return Response({'status': 'Корзина очищена'})
