from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from shop.models.order import Order
from shop.serializers.order import OrderSerializer
from shop.models.shop import Shop


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)

    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel_order(self, request, pk=None):
        order = self.get_object()
        if order.status == 'canceled':
            return Response({"detail": "Order is already canceled."}, status=status.HTTP_400_BAD_REQUEST)
        order.status = 'canceled'
        order.save()
        return Response({"detail": "Order has been canceled."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='confirm')
    def confirm_order(self, request, pk=None):
        order = self.get_object()
        if order.status == 'confirmed':
            return Response({"detail": "Order is already confirmed."}, status=status.HTTP_400_BAD_REQUEST)
        order.status = 'confirmed'
        order.save()
        return Response({"detail": "Order has been confirmed."}, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(client=self.request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data
        shop_id = data.get('shop')

        try:
            shop = Shop.objects.get(id=shop_id)
        except Shop.DoesNotExist:
            return Response({"error": "Shop not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
