from django.contrib import admin
from shop.models.product import Product, Category, ProductReview

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'description', 'price', 'quantity_in_stock', 'added_at']
    search_fields = ['name', 'category__label']
    list_filter = ['category', 'added_at']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'image', 'is_active']
    search_fields = ['name']
    list_filter = ['is_active']
    
@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'user', 'comment', 'rating']
    search_fields = ['product__name', 'user__email']
    list_filter = ['product', 'user', 'rating']


