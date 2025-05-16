from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from categories.models import Category, SubCategory
from .constants import (
    PRODUCT_NAME_MAX_LENGTH, PRODUCT_SLUG_MAX_LENGTH,
    STR_REPR_MAX_LENGTH,
    IMAGE_SMALL_SIZE, IMAGE_MEDIUM_SIZE, IMAGE_LARGE_SIZE,
    IMAGE_SMALL_QUALITY, IMAGE_MEDIUM_QUALITY, IMAGE_LARGE_QUALITY,
    IMAGE_FORMAT
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
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Категория',
        editable=False,
    )
    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Подкатегория'
    )
    # Поле с оригинальным изображением
    image = models.ImageField(
        upload_to='products/',
        verbose_name='Изображение продукта',
    )
    # Виртуальные (не сохраняются в БД) изображения разных размеров.
    # Генерируются на основе оригинального изображения при первом обращении.
    # Хранятся в /CACHE/images.
    image_small = ImageSpecField(
        source='image',
        processors=[ResizeToFill(*IMAGE_SMALL_SIZE)],
        format=IMAGE_FORMAT,
        options={'quality': IMAGE_SMALL_QUALITY}
    )
    image_medium = ImageSpecField(
        source='image',
        processors=[ResizeToFill(*IMAGE_MEDIUM_SIZE)],
        format=IMAGE_FORMAT,
        options={'quality': IMAGE_MEDIUM_QUALITY}
    )
    image_large = ImageSpecField(
        source='image',
        processors=[ResizeToFill(*IMAGE_LARGE_SIZE)],
        format=IMAGE_FORMAT,
        options={'quality': IMAGE_LARGE_QUALITY}
    )

    class Meta:
        ordering = ('category', 'subcategory', 'name',)
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def save(self, *args, **kwargs):
        '''
        Переопределяем метод save, чтобы автоматически
        устанавливать категорию на основе выбранной подкатегории subcategory.
        '''
        if self.subcategory:
            self.category = self.subcategory.category
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name[:STR_REPR_MAX_LENGTH]
