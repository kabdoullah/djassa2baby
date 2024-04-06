from django.contrib import admin
from shop.models.order import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'client', 'shop', 'delivery_address', 'commune', 'order_date', 'status', 'quantity']
    search_fields = ['product__name', 'client__email', 'shop__name']
    list_filter = ['status']