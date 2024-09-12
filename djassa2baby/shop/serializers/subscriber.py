from rest_framework import serializers
from users.serializers import UserSerializer
from shop.models.subscriber import SubscriberShop

class SubscriberShopSerializer(serializers.ModelSerializer):
    user  = UserSerializer(read_only=True)
    class Meta:
        model = SubscriberShop
        fields = '__all__'  
