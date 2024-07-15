from rest_framework import serializers
from shop.models.order import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price', 'shop']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, write_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'client', 'delivery_address', 'commune', 'order_date', 'status', 'items', 'total']

    def get_total(self, obj):
        return sum(item.price * item.quantity for item in obj.items.all())

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order
