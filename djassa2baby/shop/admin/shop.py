from django.contrib import admin
from shop.models.shop import Shop, ShopReview

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone_number_1', 'location', 'subscription', 'user']
    search_fields = ['name', 'email', 'phone_number_1']
    list_filter = ['subscription', 'is_active', 'can_evaluate']
    
@admin.register(ShopReview)
class ShopReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'shop', 'user', 'comment', 'rating']
    search_fields = ['shop__name', 'user__email']
    list_filter = ['shop', 'user', 'rating']



