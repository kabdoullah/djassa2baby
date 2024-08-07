from rest_framework import serializers
from shop.models.order import Order, OrderItem
from users.models import User



class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number']
        
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price', 'shop']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, write_only=True)
    total = serializers.SerializerMethodField()
    client = ClientSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'client', 'delivery_address', 'commune', 'order_date', 'status', 'items', 'total', 'note']

    def get_total(self, obj):
        return sum(item.price * item.quantity for item in obj.items.all())

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order

class AnonymousOrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, write_only=True)
    total = serializers.SerializerMethodField()

    full_name = serializers.CharField(max_length=255)
    note = serializers.CharField(max_length=255, allow_blank=True, required=False)

    class Meta:
        model = Order
        fields = ['id', 'full_name', 'delivery_address', 'commune', 'order_date', 'status', 'items', 'total', 'note']

    def get_total(self, obj):
        return sum(item.price * item.quantity for item in obj.items.all())

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order