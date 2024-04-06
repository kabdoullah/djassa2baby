import uuid
from django.db import models
from users.models import User


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    reduced_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    image1 = models.ImageField(
        upload_to='product_images/', null=True, blank=True)
    image2 = models.ImageField(
        upload_to='product_images/', null=True, blank=True)
    image3 = models.ImageField(
        upload_to='product_images/', null=True, blank=True)
    image4 = models.ImageField(
        upload_to='product_images/', null=True, blank=True)
    image5 = models.ImageField(
        upload_to='product_images/', null=True, blank=True)
    quantity_in_stock = models.IntegerField()
    instock = models.BooleanField(default=True)
    added_at = models.DateTimeField(auto_now_add=True)
    # Champ pour stocker la note moyenne
    average_rating = models.DecimalField(
        max_digits=3, decimal_places=2, default=0.00)
    total_ratings = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class ProductReview(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.IntegerField()