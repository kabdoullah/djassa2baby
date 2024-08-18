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

        #fields = ['id', 'client', 'delivery_address', 'commune', 'phone_number','order_date', 'status', 'items', 'total', 'note']

        fields = ['id', 'client','ref_order', 'delivery_address', 'commune', 'order_date', 'status', 'items', 'total', 'note']

    @staticmethod
    def get_total(obj):
        return sum(item.price * item.quantity for item in obj.items.all())
    
    def generate_order_number(self):
        # Exemple de génération de numéro de commande unique
        from uuid import uuid4
        return f'ORD-{uuid4().hex[:10].upper()}'

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        validated_data['ref_order'] = self.generate_order_number()
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

        #fields = ['id', 'full_name', 'delivery_address', 'commune', 'phone_number','order_date', 'status', 'items', 'total', 'note']

        fields = ['id','ref_order', 'full_name', 'delivery_address', 'commune','phone_number', 'order_date', 'status', 'items', 'total', 'note']


    @staticmethod
    def get_total(obj):
        return sum(item.price * item.quantity for item in obj.items.all())
    
    def generate_order_number(self):
        # Exemple de génération de numéro de commande unique
        from uuid import uuid4
        return f'ORD-{uuid4().hex[:10].upper()}'

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        # Génération d'un numéro de commande unique
        validated_data['ref_order'] = self.generate_order_number()
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order