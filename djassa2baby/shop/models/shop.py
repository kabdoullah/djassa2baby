import uuid
from django.db import models
from users.models import User
from shop.models.subscription import Subscription
from django.utils.text import slugify


class Shop(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='shop_logos/')
    email = models.EmailField()
    phone_number_1 = models.CharField(max_length=20)
    phone_number_2 = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    facebook_link = models.URLField(blank=True, null=True)
    whatsapp_link = models.URLField(blank=True, null=True)
    instagram_link = models.URLField(blank=True, null=True)
    twitter_link = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    can_evaluate = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ShopReview(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(blank=True, null=True)
    rating = models.IntegerField()
