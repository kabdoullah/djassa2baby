from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from shop.models.order import Order
from shop.serializers.order import OrderSerializer, AnonymousOrderSerializer
from shop.permissions.permission import IsClient, IsSeller
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.action in ['client_orders', 'create', 'cancel']:
            self.permission_classes = [IsAuthenticated, IsClient]
        elif self.action == 'shop_orders':
            self.permission_classes = [IsAuthenticated, IsSeller]
        else:
            self.permission_classes = [IsAuthenticated]
        return super(OrderViewSet, self).get_permissions()

    def get_queryset(self):
        if self.action == 'client_orders':
            return Order.objects.filter(client=self.request.user)
        return super(OrderViewSet, self).get_queryset()

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = get_object_or_404(Order, pk=pk, client=request.user)
        if order.status in ['pending', 'confirmed']:
            order.status = 'canceled'
            order.save()
            return Response({'status': 'Order canceled'}, status=status.HTTP_200_OK)
        return Response({'error': 'Order cannot be canceled'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='client-orders')
    def client_orders(self, request):
        orders = self.get_queryset()
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='shop-orders/(?P<shop_id>[^/.]+)')
    def shop_orders(self, request, shop_id=None):
        orders = Order.objects.filter(items__shop_id=shop_id).distinct()
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

class CreateAnonymousOrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = AnonymousOrderSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = AnonymousOrderSeriaselizer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            for item in request.data.get('items', []):
                product = Product.objects.get(id=item['product'])
                OrderItem.objects.create(order=order, product=product, quantity=item['quantity'], price=product.price)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)