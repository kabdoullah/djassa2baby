from shop.models.shop import Shop
from rest_framework import serializers
from shop.models.product import Product, Category, ProductReview,ShopCategorie
from shop.serializers.shop import ShopSerializer
from users.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
    

class ProductResponseSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    shop = ShopSerializer(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


class ProductReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = ProductReview
        fields = '__all__'

class ProductReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        fields = '__all__'
        

class ShopCategorieSerializer(serializers.ModelSerializer):
    # On utilise les IDs pour les catégories et les magasins lors de la création ou mise à jour
    category = CategorySerializer(read_only=True)
    shop = ShopSerializer(read_only=True)

    class Meta:
        model = ShopCategorie
        fields = ['id', 'category', 'shop', 'is_active', 'added_at']

