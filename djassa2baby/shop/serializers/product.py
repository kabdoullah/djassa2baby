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

    def create(self, validated_data):
        categories = validated_data.pop('categories', []) #array of the id (uid) of the category selected
        shop_id = validated_data.pop('shop_id')
        shop = Shop.objects.get(id=shop_id)

        shop_categories = []

        for categorie in categories:
            category = Category.objects.get(id=categorie)
            shop_categories.append(ShopCategorie(category=category, shop=shop, **validated_data))
        
          # Utilisation de bulk_create pour créer plusieurs ShopCategorie en une seule requête
        ShopCategorie.objects.bulk_create(shop_categories)

        return shop_categories
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['categories'] = CategorySerializer(instance.category).data
        response['shop'] = ShopSerializer(instance.shop).data
        return response
       
