from rest_framework import serializers
from shop.models.product import Product, Category, Image

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'label', 'description', 'is_active']
        
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'