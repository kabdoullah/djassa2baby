from django.contrib import admin
from shop.models.subscriber import SubscriberShop

@admin.register(SubscriberShop)
class SubscriberShopAdmin(admin.ModelAdmin):
    pass
    
