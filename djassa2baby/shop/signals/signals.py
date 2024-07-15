from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from shop.models.order import OrderItem

@receiver(post_save, sender=OrderItem)
def increase_product_stock(sender, instance, created, **kwargs):
    if created:
        instance.product.quantity_in_stock -= instance.quantity
        instance.product.save()

@receiver(post_delete, sender=OrderItem)
def decrease_product_stock(sender, instance, **kwargs):
    instance.product.quantity_in_stock += instance.quantity
    instance.product.save()
