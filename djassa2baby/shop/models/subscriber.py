from django.db import models
from users.models import User
from shop.models.shop import Shop

class SubscriberShop(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='subscribers')
    fcm_token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)  # Indicates if the subscription is currently active
    receive_notifications = models.BooleanField(default=True)  # Opt-in for notifications

    # Additional fields can be added as needed, for example, notification frequency
    NOTIFICATION_FREQUENCY_CHOICES = [
        ('instant', 'Instant'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
    ]
    
    notification_frequency = models.CharField(
        max_length=10,
        choices=NOTIFICATION_FREQUENCY_CHOICES,
        default='instant'
    )

    class Meta:
        unique_together = ('user', 'shop')  # Prevents duplicate subscriptions

    def __str__(self):
        return f"{self.user.username} subscribed to {self.shop.name} on {self.created_at.date()}"
