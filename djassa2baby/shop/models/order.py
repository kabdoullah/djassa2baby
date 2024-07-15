import uuid
from django.db import models
from shop.models.product import Product
from shop.models.shop import Shop
from users.models import User


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('canceled', 'Canceled'),
        ('delivered', 'Delivered'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_address = models.CharField(max_length=255)
    commune = models.CharField(max_length=100)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=30, choices=STATUS_CHOICES, default='pending')



class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='orders', null=True)
    
