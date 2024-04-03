from django.contrib import admin
from core.models.role import Role

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['id', 'label']

