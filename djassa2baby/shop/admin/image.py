from django.contrib import admin
from shop.models.product import Image

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'image']
    search_fields = ['product__name']
    list_filter = ['product']