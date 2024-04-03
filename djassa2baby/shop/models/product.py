import uuid
from django.db import models

class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey('Product', related_name='product_images', on_delete=models.CASCADE,null=True, blank=True)
    image = models.ImageField(upload_to='product_images/')

    
class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    label = models.CharField(max_length=100)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.label

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE) 
    price = models.DecimalField(max_digits=10, decimal_places=2)
    reduced_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # images = models.ManyToManyField(Image)
    quantity_in_stock = models.IntegerField()
    instock = models.BooleanField(default=True)
    added_at = models.DateTimeField(auto_now_add=True)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)  # Champ pour stocker la note moyenne
    total_ratings = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
    

