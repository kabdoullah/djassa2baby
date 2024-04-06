from django.contrib import admin
from shop.models.subscription import Subscription, SubscriptionHistory


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'description', 'is_active']
    search_fields = ['name', 'description']
    list_filter = ['is_active']


@admin.register(SubscriptionHistory)
class SubscriptionHistoryAdmin(admin.ModelAdmin):
    list_display = ['shop', 'subscription', 'payment_date']
    search_fields = ['shop__name', 'subscription__label']
    list_filter = ['payment_date']
