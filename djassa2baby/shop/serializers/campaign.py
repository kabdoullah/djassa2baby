from djassa2baby.shop.models.campaign import Campaign
from djassa2baby.shop.models.product import Product
from shop.serializers.product import ProductSerializer
from rest_framework import serializers


class CampaignSerializer(serializers.ModelSerializer):
    target_products = ProductSerializer(many=True, read_only=True)  # Pour afficher les informations des produits ciblés
    target_product_ids = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), many=True, write_only=True, source='target_products')

    class Meta:
        model = Campaign
        fields = ['id', 'name', 'campaign_type', 'target_products', 'target_product_ids', 'discount', 'start_date', 'end_date', 'created_at', 'updated_at']


    def validate(self, data):
        """
        Validate the data before saving
        """
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("La date de début ne peut pas être après la date de fin.")
        if data['discount'] < 0:
            raise serializers.ValidationError("Le montant de la réduction ne peut pas être négatif.")

        return data
    

    def create(self, validated_data):
        target_products = validated_data.pop('target_products')
        campaign = Campaign.objects.create(**validated_data)
        campaign.target_products.set(target_products)
        return campaign

    def update(self, instance, validated_data):
        target_products = validated_data.pop('target_products', None)
        if target_products is not None:
            instance.target_products.set(target_products)
        return super().update(instance, validated_data)