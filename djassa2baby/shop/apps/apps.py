from django.apps import AppConfig
from shop.signals.signals import increase_product_stock, decrease_product_stock



class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop'
    



default_app_config = 'shop.apps.ShopConfig'