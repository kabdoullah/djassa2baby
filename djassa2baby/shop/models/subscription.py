import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _



class Subscription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    

class SubscriptionHistory(models.Model):
    subscription = models.ForeignKey('Subscription', on_delete=models.CASCADE)
    shop = models.ForeignKey('shop.Shop', on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Subscription History')
        verbose_name_plural = _('Subscription Histories')

    def __str__(self):
        return f'{self.user} - {self.subscription} - {self.payment_date}'