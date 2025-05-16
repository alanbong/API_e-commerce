from django.db import models

from categories.models import Category, SubCategory
from .constants import (
    PRODUCT_NAME_MAX_LENGTH,
    PRODUCT_SLUG_MAX_LENGTH,
    STR_REPR_MAX_LENGTH,
)


class Product(models.Model):
    '''
    Модель для продуктов
    '''
    name = models.CharField(
        max_length=PRODUCT_NAME_MAX_LENGTH,
        unique=True,
        verbose_name='Название продукта',
    )
    slug = models.SlugField(
        max_length=PRODUCT_SLUG_MAX_LENGTH,
        unique=True,
        verbose_name='Идентификатор продукта',
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание продукта',
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена продукта в рублях',
    )
    image_large = models.ImageField(
        upload_to='products/large/',
        verbose_name='Изображение (большое)',
    )
    image_medium = models.ImageField(
        upload_to='products/medium/',
        verbose_name='Изображение (среднее)',
    )
    image_small = models.ImageField(
        upload_to='products/small/',
        verbose_name='Изображение (маленькое)',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Категория',
    )
    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Подкатегория'
    )

    class Meta:
        ordering = ('category', 'subcategory', 'name',)
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name[:STR_REPR_MAX_LENGTH]
