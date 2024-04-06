from rest_framework import viewsets
from rest_framework import permissions
from shop.models.order import Order
from shop.serializers.order import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
