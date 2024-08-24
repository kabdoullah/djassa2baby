
import uuid
from django.db import models
from shop.models.shop import Shop

from djassa2baby.shop.models.product import Product

class Campaign(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='campaigns')
    name = models.CharField(max_length=100)
    campaign_type = models.CharField(max_length=50)  # Ex: 'discount', 'flash_sale'
    target_products = models.ManyToManyField(Product)
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
