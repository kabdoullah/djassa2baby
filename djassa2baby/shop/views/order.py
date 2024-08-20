from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from shop.models.order import Order
from users.models import User
from shop.permissions.permission import IsClient, IsSeller
from shop.serializers.order import OrderSerializer, OrderResponseSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        match self.action:
            case 'client_orders', 'cancel':
                self.permission_classes = [IsAuthenticated, IsClient]
            case 'shop_orders':
                self.permission_classes = [IsAuthenticated, IsSeller]
            case 'create':
                self.permission_classes = [AllowAny]
            case _:
                self.permission_classes = [IsAuthenticated]
        return super(OrderViewSet, self).get_permissions()

    def get_queryset(self):
        if self.action == 'client_orders':
            return Order.objects.filter(client=self.request.user)
        return super(OrderViewSet, self).get_queryset()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = get_object_or_404(Order, pk=pk, client=request.user)
        if order.status in ['pending', 'confirmed']:
            order.status = 'canceled'
            order.save()
            return Response({'status': 'Order canceled'}, status=status.HTTP_200_OK)
        return Response({'error': 'Order cannot be canceled'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='client-orders')
    def client_orders(self):
        orders = self.get_queryset()
        serializer = OrderResponseSerializer(orders, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='shop-orders/(?P<shop_id>[^/.]+)')
    def shop_orders(self, shop_id=None):
        orders = Order.objects.filter(items__shop_id=shop_id).distinct()
        serializer = OrderResponseSerializer(orders, many=True)
        return Response(serializer.data)
