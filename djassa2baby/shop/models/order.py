import uuid

from django.db import models
from core.models.coupon import Coupon
from shop.models.product import Product

from shop.models.shop import Shop
from users.models import User


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('confirmed', 'Confirmée'),
        ('canceled', 'Annulée'),
        ('delivered', 'Livrée'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ref_order = models.CharField(max_length=100, blank=True, null=True)
    client = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    delivery_address = models.CharField(max_length=255)
    coupon_code = models.CharField(max_length=50, null=True, blank=True)
    commune = models.CharField(max_length=100)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending')
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    total_price = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    note = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Vérifiez si un code coupon est associé à la commande
        if self.coupon_code:
            try:
                coupon = Coupon.objects.get(coupon_code=self.coupon_code)
                # Vérifiez si le coupon est actif et si le nombre d'activations n'est pas atteint
                if coupon.is_active and coupon.nombre_activation < coupon.max_activation:
                    coupon.increment_activation()
                else:
                    raise ValueError("Le coupon n'est plus valide.")
            except Coupon.DoesNotExist:
                raise ValueError("Le coupon n'existe pas.")
        
        # Appelez la méthode save originale
        super(Order, self).save(*args, **kwargs)



class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=20, decimal_places=2)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='orders', null=True)
