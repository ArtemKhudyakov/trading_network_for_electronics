from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Product, NetworkNode


class ProductInline(admin.TabularInline):
    model = NetworkNode.products.through
    extra = 1
    verbose_name = "Продукт"
    verbose_name_plural = "Продукты"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'model', 'release_date']
    list_filter = ['release_date']
    search_fields = ['name', 'model']


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'get_level_display',
        'supplier_link',
        'debt',
        'created_at',
        'city'
    ]
    list_filter = ['city', 'level', 'created_at', 'country']
    search_fields = ['name', 'email', 'country', 'city']
    inlines = [ProductInline]
    actions = ['clear_debt']
    exclude = ('products',)

    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'level', 'supplier')
        }),
        ('Контактная информация', {
            'fields': ('email', 'country', 'city', 'street', 'house_number')
        }),
        ('Финансы', {
            'fields': ('debt',)
        }),
    )

    def supplier_link(self, obj):
        if obj.supplier:
            url = reverse('admin:trading_network_networknode_change', args=[obj.supplier.id])
            return format_html('<a href="{}">{}</a>', url, obj.supplier.name)
        return "Нет поставщика"

    supplier_link.short_description = "Поставщик"

    def clear_debt(self, request, queryset):
        updated_count = queryset.update(debt=0)
        self.message_user(request, f'Задолженность очищена у {updated_count} объектов')

    clear_debt.short_description = "Очистить задолженность перед поставщиком"