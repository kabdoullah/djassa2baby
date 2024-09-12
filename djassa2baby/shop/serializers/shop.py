from rest_framework import serializers
from core.models.role import Role
from users.utils import send_otp_email
from shop.models.otp import OtpCode
from shop.models.product import Category, ShopCategorie
from shop.models.subscription import Subscription
from users.models import User
from shop.models.shop import Shop, ShopReview
import ast
from django.db import transaction, IntegrityError

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = [
            'id', 'name', 'logo', 'email', 'phone_number_1', 'phone_number_2',
            'description', 'location', 'facebook_link',
            'whatsapp_link', 'instagram_link', 'twitter_link', 'is_active',
            'can_evaluate', 'date_added', 'user', 'slug'
        ]
        
        extra_kwargs = {
            'logo': {'required': False, 'allow_null': True},
            'slug': {'read_only': True},
            'date_added': {'read_only': True},
            'is_active': {'read_only': True},
            'can_evaluate': {'read_only': True},
            'user': {'read_only': True}
        }


class ShopReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopReview
        fields = '__all__'


import random


def generate_otp():

    """Génère un code OTP à 6 chiffres."""
    
    return str(random.randint(100000, 999999))



class ShopOwnerSerializer(serializers.Serializer):

    """
    Serializer for creating a shop with an owner.
    """
    name = serializers.CharField(max_length=255)
    logo = serializers.ImageField(required=True)
    email = serializers.EmailField()
    phone_number_1 = serializers.CharField(max_length=20)
    password = serializers.CharField(write_only=True)  # Write-only to avoid exposing it
    phone_number_2 = serializers.CharField(max_length=20, required=False, allow_null=True)
    description = serializers.CharField(required=False, allow_blank=True)
    location = serializers.CharField(max_length=255)
    subscription = serializers.UUIDField(required=False, allow_null=True)
    facebook_link = serializers.URLField(required=False, allow_null=True)
    whatsapp_link = serializers.URLField(required=False, allow_null=True)
    instagram_link = serializers.URLField(required=False, allow_null=True)
    twitter_link = serializers.URLField(required=False, allow_null=True)
    categories = serializers.CharField( required=False, allow_null=True)  # New field

    def create(self, validated_data):
        try:
            # Démarrer une transaction atomique
            with transaction.atomic():
                # Extract password and handle user creation separately
                password = validated_data.pop('password')
                categories = validated_data.pop('categories', None)
                # Create the user associated with this shop
                vendor_role = Role.objects.get(label='vendeur')  # Assuming role retrieval is correct
                subscription = Subscription.objects.get(name='Gratuit')

                user = User.objects.create_user(
                    phone_number=validated_data['phone_number_1'],
                    password=password,
                    email=validated_data.get('email'),
                    role=vendor_role
                )
                
                # Assign the user to the validated data and create the shop
                validated_data['user'] = user
                validated_data['subscription'] = subscription
                shop = Shop.objects.create(**validated_data)
                
                #create otp to verify the store account 
                otp = OtpCode(
                    otp = generate_otp(),
                    shop = shop,
                )

                otp.save()
                # Convert the categories string back to a list of UUIDs
                liste_uuids = ast.literal_eval(categories)
                # Handle categories
                for categorie_id in liste_uuids:
                    category = Category.objects.get(id=categorie_id)
                    ShopCategorie.objects.create(
                        shop=shop,
                        category=category
                    )

                # Envoi de l'email
                send_otp_email(shop, otp.otp)

                return shop

        except IntegrityError as e:
            # Gérer l'erreur d'intégrité, par exemple les duplications de clé ou les erreurs de contrainte
            print(f"IntegrityError occurred: {str(e)}")
            raise serializers.ValidationError("Une erreur s'est produite lors de la création de la boutique.")

        except Exception as e:
            # Gérer toute autre erreur
            print(f"An error occurred: {str(e)}")
            raise serializers.ValidationError("Une erreur s'est produite lors de la création de la boutique.")

