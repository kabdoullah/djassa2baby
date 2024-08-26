from django.contrib import admin
from shop.models.campaign import Campaign

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    pass
    

    