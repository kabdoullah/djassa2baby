from rest_framework import serializers
from shop.models.order import Order, OrderItem
from users.models import User


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'phone_number']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price', 'shop']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, write_only=True)
    total_price = serializers.SerializerMethodField(read_only=True)
    full_name = serializers.CharField(max_length=100, write_only=True)

    class Meta:
        model = Order
        fields = ['full_name', 'phone_number', 'delivery_address', 'commune', 'items', 'total_price', 'note']

    @staticmethod
    def generate_order_number():
        # Exemple de génération de numéro de commande unique
        from uuid import uuid4
        return f'ORD-{uuid4().hex[:10].upper()}'""


    def get_total_price(self, obj):
        return sum(item.price * item.quantity for item in obj.items.all())



    def create(self, validated_data):
        items_data = validated_data.pop('items')
        validated_data['ref_order'] = self.generate_order_number()
        # Décomposer le full_name en first_name et last_name
        full_name = validated_data.pop('full_name')
        first_name, last_name = full_name.split(' ', 1) if ' ' in full_name else (full_name, '')

        # Si l'utilisateur est authentifié, utilisez l'utilisateur actuel comme client
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            client = request.user
        else:
            phone_number = validated_data.get('phone_number')
            # Créer ou récupérer un utilisateur anonyme basé sur first_name et phone_number
            client, created = User.objects.get_or_create(
                first_name=first_name,
                last_name=last_name,
                defaults={'phone_number': phone_number}
            )

        # Créer la commande avec le client
        order = Order.objects.create(client=client, **validated_data)

        # Créer les OrderItems
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order


class OrderResponseSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    client = ClientSerializer(read_only=True)

    class Meta:
        model = Order
<<<<<<< HEAD
        #fields = ['id', 'client', 'delivery_address', 'commune', 'phone_number','order_date', 'status', 'items', 'total', 'note']

        fields = ['id', 'client','ref_order', 'delivery_address', 'commune', 'order_date', 'status', 'items', 'total', 'note']

    def get_total(self, obj):
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
        fields = ['id','ref_order', 'full_name', 'delivery_address', 'coupon_code','commune','phone_number', 'order_date', 'status', 'items', 'total', 'note']


    def get_total(self, obj):
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
=======
        fields = ['id', 'ref_order', 'client', 'delivery_address', 'commune', 'phone_number', 'order_date', 'status',
                  'total_price',
                  'items', 'note'
                  ]
>>>>>>> 9a3759cac4f1c7f7ad2d8594f681cc397deb39e6
