from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


from products.models import Product
from .constants import MAX_PRODUCT_QUANTITY_VALUE


User = get_user_model()


class Cart(models.Model):
    """
    Модель корзины.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Пользователь',
    )

    class Meta:
        ordering = ('user',)
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f'Корзина пользователя {self.user}'


class CartItem(models.Model):
    """
    Товар в корзине.
    """
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Корзина'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='cart_item',
        verbose_name='Товар в корзине'
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name='Количество товаров',
        validators=[
            MinValueValidator(
                1, message=(
                    'Минимальное количество товаров - 1'
                )
            ),
            MaxValueValidator(
                MAX_PRODUCT_QUANTITY_VALUE, message=(
                    'Максимальное количество товаров - 9999'
                )
            )
        ]
    )

    class Meta:
        ordering = ('product',)
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'
        constraints = [
            models.UniqueConstraint(
                fields=('cart', 'product'),
                name='unique_cart_product'
            )
        ]

    def __str__(self):
        return (
            f'{self.product.name} {self.quantity}шт. '
            f'в корзине {self.cart.user}'
        )
