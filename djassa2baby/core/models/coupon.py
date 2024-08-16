import uuid
from django.db import models

from shop.models.shop import Shop


class Coupon(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    coupon_code = models.CharField(max_length=50)
    shop = models.ForeignKey('shop.Shop', on_delete=models.CASCADE, null=True)
    reduction = models.DecimalField(max_digits=10, decimal_places=2)
    shop = models.ForeignKey(
        Shop, on_delete=models.CASCADE, null=True, blank=True, related_name='shop_coupons') # ajout d ela boutique sur le coupon 
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
