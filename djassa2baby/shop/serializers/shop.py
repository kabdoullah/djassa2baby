from rest_framework import serializers
from shop.models.shop import Shop, ShopReview


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'


class ShopReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopReview
        fields = ['id', 'shop', 'user', 'comment', 'rating']
