from django.contrib import admin
from core.models.coupon import Coupon

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'discount', 'start_date', 'end_date', 'is_active']
    search_fields = ['code']
    list_filter = ['start_date', 'end_date', 'is_active']