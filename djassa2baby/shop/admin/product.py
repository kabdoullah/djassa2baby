from django.contrib import admin
from shop.models.product import Product, Category

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'description', 'price', 'quantity_in_stock', 'added_at']
    search_fields = ['name', 'category__label']
    list_filter = ['category', 'added_at']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'label', 'description', 'is_active']
    search_fields = ['label']
    list_filter = ['is_active']


