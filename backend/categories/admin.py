from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, SubCategory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Админка для модели Category.
    Автозаполнение slug.
    """
    list_display = ('name', 'slug', 'image_preview')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'slug')
    ordering = ('name',)

    @admin.display(description='Превью')
    def image_preview(self, obj):
        """
        Отображает уменьшенное изображение категории в админке.
        """
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" style="height: 40px;" />'
            )
        return 'Нет изображения'
    image_preview.short_description = 'Превью'


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    """
    Админка для модели SubCategory.
    Автозаполнение slug, фильтр по категории.
    """
    list_display = ('name', 'slug', 'image_preview')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('category',)
    search_fields = ('name', 'slug')

    ordering = ('name',)
    autocomplete_fields = ('category',)

    @admin.display(description='Превью')
    def image_preview(self, obj):
        """
        Отображает уменьшенное изображение подкатегории в админке.
        """
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" style="height: 40px;" />'
            )
        return 'Нет изображения'
