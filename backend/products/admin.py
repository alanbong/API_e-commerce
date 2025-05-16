from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Админка для модели Product.
    Автозаполнение slug.
    Категория вычисляется автоматически из подкатегории.
    """
    list_display = ('name', 'subcategory', 'category', 'price', 'image_preview')
    readonly_fields = ('category',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'slug')
    list_filter = ('category', 'subcategory')
    ordering = ('category', 'subcategory', 'name',)

    @admin.display(description='Превью')
    def image_preview(self, obj):
        """
        Отображает уменьшенное изображение товара в админке.
        """
        if obj.image_small:
            return mark_safe(
                f'<img src="{obj.image_small.url}" style="height: 40px;" />'
            )
        return 'Нет изображения'
