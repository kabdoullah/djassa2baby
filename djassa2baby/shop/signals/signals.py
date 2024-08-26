from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from shop.models.subscriber import SubscriberShop
from shop.models.product import Product
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

from firebase_admin import messaging

def notify_new_product(product):
    store = product.store
    subscriptions = SubscriberShop.objects.filter(store=store)

    for subscription in subscriptions:
        message = messaging.Message(
            notification=messaging.Notification(
                title=f'Nouveau produit dans {store.name}',
                body=f'{product.name} vient d\'être ajouté.',
            ),
            token=subscription.fcm_token,
        )
        response = messaging.send(message)
        print(f'Notification envoyée à {subscription.user.username}: {response}')




@receiver(post_save, sender=Product)
def send_new_product_notification(sender, instance, created, **kwargs):
    if created:
        notify_new_product(instance)
