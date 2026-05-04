from django.contrib import admin
from .models import Product, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'tipo', 'stock')
    search_fields = ('nombre',)
    list_filter = ('tipo',)


admin.site.register(Category)
