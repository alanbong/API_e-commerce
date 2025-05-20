from django.contrib import admin

from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    """
    Вложенное отображение элементов корзины
    в карточке Cart.
    """
    model = CartItem
    extra = 0
    readonly_fields = ('product', 'quantity')
    can_delete = False


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """
    Админка для модели Cart.
    """
    list_display = ('user',)
    search_fields = ('user__username', 'user__email')
    inlines = [CartItemInline]

    @admin.display(description='Количество товаров')
    def total_items(self, obj):
        return obj.items.count()

    @admin.display(description='Общая стоимость')
    def total_price(self, obj):
        return sum(item.product.price * item.quantity for item in obj.items.all())

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    '''
    Админка для отладки и сбора данных модели CartItem.
    Фильтрация по товарам и корзинам.
    Только чтение.
    '''
    list_display = ('cart', 'product', 'quantity')
    list_filter = ('cart', 'product')
    search_fields = ('product__name', 'cart__user__username')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
