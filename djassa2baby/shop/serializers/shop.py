from rest_framework import serializers
from core.models.role import Role
from shop.models.subscription import Subscription
from users.models import User
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


class ShopOwnerSerializer(serializers.Serializer):
    """
        Serializer for creating a shop with an owner.
    """
    name = serializers.CharField(max_length=255)
    logo = serializers.ImageField(required=False)
    email = serializers.EmailField()
    phone_number_1 = serializers.CharField(max_length=20)
    password = serializers.CharField(write_only=True)  # Write-only to avoid exposing it
    phone_number_2 = serializers.CharField(max_length=20, required=False, allow_null=True)
    description = serializers.CharField(required=False, allow_blank=True)
    location = serializers.CharField(max_length=255)
    subscription = serializers.UUIDField(required=False,allow_null=True)
    facebook_link = serializers.URLField(required=False, allow_null=True)
    whatsapp_link = serializers.URLField(required=False, allow_null=True)
    instagram_link = serializers.URLField(required=False, allow_null=True)
    twitter_link = serializers.URLField(required=False, allow_null=True)

    def create(self, validated_data):
        # Extract password and handle user creation separately
        password = validated_data.pop('password')
        # Create the user associated with this shop
        vendror_role = Role.objects.get(label='vendeur')  # Assuming role retrieval is correct
        subscription = Subscription.objects.get(name='Gratuit')

        user = User.objects.create_user(
            phone_number=validated_data['phone_number_1'],
            password=password,
            email=validated_data.get('email'),
            role=vendror_role
        )
        
        # Assign the user to the validated data and create the shop
        validated_data['user'] = user
        validated_data['subscription'] = subscription
        return Shop.objects.create(**validated_data)


