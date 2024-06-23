from rest_framework import serializers
from shop.models.order import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']

    def validate(self, data):
        product = data['product']
        quantity = data['quantity']

        if not product.is_available(quantity):
            raise serializers.ValidationError(
                "Ce produit n'est pas disponible en quantité suffisante.")

        return data


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    client = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'client', 'shop', 'delivery_address',
                  'commune', 'order_date', 'status', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        print("validated_data", validated_data)
        print('items_data', items_data)
        order = Order.objects.create(**validated_data)
        print('order', order)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order
