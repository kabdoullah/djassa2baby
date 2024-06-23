from django.contrib import admin
from shop.models.order import Order, OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'client', 'shop', 'delivery_address', 'commune', 'order_date', 'status', 'quantity']
    search_fields = ['product__name', 'client__email', 'shop__name']
    list_filter = ['status']
    date_hierarchy = 'order_date'
    readonly_fields = ['order_date']
    
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']
    search_fields = ['order__id', 'product__name']
    list_filter = ['product']
    readonly_fields = ['price']
    