from django.db import models

from .constants import (
    CATEGORY_NAME_MAX_LENGTH,
    CATEGORY_SLUG_MAX_LENGTH,
    SUBCATEGORY_NAME_MAX_LENGTH,
    SUBCATEGORY_SLUG_MAX_LENGTH,
    STR_REPR_MAX_LENGTH
)


class Category(models.Model):
    """
    Модель для категорий товаров.
    """

    name = models.CharField(
        max_length=CATEGORY_NAME_MAX_LENGTH,
        unique=True,
        verbose_name='Название категории',
    )
    slug = models.SlugField(
        max_length=CATEGORY_SLUG_MAX_LENGTH,
        unique=True,
        verbose_name='Идентификатор категории',
    )
    image = models.ImageField(
        upload_to='categories/',
        verbose_name='Изображение категории',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name[:STR_REPR_MAX_LENGTH]


class SubCategory(models.Model):
    """
    Модель для подкатегорий товаров.
    """

    name = models.CharField(
        max_length=SUBCATEGORY_NAME_MAX_LENGTH,
        unique=True,
        verbose_name='Название подкатегории',
    )
    slug = models.SlugField(
        max_length=SUBCATEGORY_SLUG_MAX_LENGTH,
        unique=True,
        verbose_name='Идентификатор подкатегории',
    )
    image = models.ImageField(
        upload_to='subcategories/',
        verbose_name='Изображение подкатегории',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='subcategories',
        verbose_name='Родительская категория',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Податегория'
        verbose_name_plural = 'Подкатегории'

    def __str__(self):
        return self.name[:STR_REPR_MAX_LENGTH]
