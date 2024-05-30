import uuid
from django.db import models
from users.models import User
from shop.models.shop import Shop
from django.utils.text import slugify


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(
        upload_to='category_images/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True, blank=True, related_name='products')
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
    average_rating = models.DecimalField(
        max_digits=3, decimal_places=2, default=0.00)
    total_ratings = models.PositiveIntegerField(default=0)
    slug = models.SlugField(unique=True, max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductReview(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    comment = models.TextField(blank=True, null=True)
    rating = models.IntegerField()
    added_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
