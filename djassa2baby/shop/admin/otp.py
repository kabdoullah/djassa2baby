from django.contrib import admin
from shop.models.otp import OtpCode

@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ['id', 'otp', 'shop', 'is_active', 'created_at', 'expires_at',]
    search_fields = ['otp', 'shop__email', 'otp__created_at']
    list_filter = ['expires_at']
    date_hierarchy = 'created_at'
