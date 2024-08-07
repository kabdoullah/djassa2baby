from rest_framework import serializers
from shop.models.shop import Shop, ShopReview


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = [
            'id', 'name', 'logo', 'email', 'phone_number_1', 'phone_number_2',
            'description', 'location', 'subscription', 'facebook_link', 
            'whatsapp_link', 'instagram_link', 'twitter_link', 'is_active',
            'can_evaluate', 'date_added', 'user', 'slug'
        ]
        extra_kwargs = {
            'logo': {'required': False, 'allow_null': True},
            'user': {'required': False, 'allow_null': True},
            'subscription': {'required': False, 'allow_null': True}
        }

class ShopReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopReview
        fields = '__all__'
