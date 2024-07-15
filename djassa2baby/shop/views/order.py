from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from shop.models.order import Order
from shop.serializers.order import OrderSerializer
from shop.models.shop import Shop
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Vérifie que l'utilisateur est authentifié avant de filtrer les commandes
        if self.request.user.is_authenticated:
            return Order.objects.filter(client=self.request.user)
        return Order.objects.none()

    def perform_create(self, serializer):
        # Assure que l'utilisateur est authentifié avant de créer une commande
        if self.request.user.is_authenticated:
            serializer.save(client=self.request.user)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        # Vérifie que l'utilisateur est authentifié avant d'annuler une commande
        if request.user.is_authenticated:
            order = get_object_or_404(Order, pk=pk, client=request.user)
            if order.status in ['pending', 'confirmed']:
                order.status = 'canceled'
                order.save()
                return Response({'status': 'Order canceled'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Order cannot be canceled'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)