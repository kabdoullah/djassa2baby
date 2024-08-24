from rest_framework import serializers
from shop.models.subscriber import SubscriberShop

class SubscriberShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriberShop
        fields = '__all__'  # You can specify the exact fields if not all are needed
