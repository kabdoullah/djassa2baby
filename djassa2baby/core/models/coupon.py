import uuid
from django.db import models

from shop.models.shop import Shop


class Coupon(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    coupon_code = models.CharField(max_length=50)
    shop = models.ForeignKey('shop.Shop', on_delete=models.CASCADE, null=True)
    nombre_activation = models.IntegerField(default=0)
    max_activation = models.IntegerField(default=1)
    reduction = models.DecimalField(max_digits=10, decimal_places=2)
    shop = models.ForeignKey(
        Shop, on_delete=models.CASCADE, null=True, blank=True, related_name='shop_coupons') # ajout d ela boutique sur le coupon 
    start_date = models.DateField()
    end_date = models.DateField()
    is_publish = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def increment_activation(self):

        """
            Incrémente le nombre d'activations et désactive le coupon si le maximum est atteint.
        
        """

        if self.nombre_activation < self.max_activation:
            self.nombre_activation += 1
            self.save()
        if self.nombre_activation >= self.max_activation:
            self.is_active = False
            self.save()