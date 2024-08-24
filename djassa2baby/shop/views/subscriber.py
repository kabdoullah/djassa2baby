from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from shop.models.subscriber import SubscriberShop
from shop.serializers.subscriber import SubscriberShopSerializer
from shop.models.shop import Shop
class SubscriberShopViewSet(ModelViewSet):
    queryset = SubscriberShop.objects.all()
    serializer_class = SubscriberShopSerializer

    @action(detail=False, methods=['post'], url_path='subscribe')
    def subscribe(self, request):
        user = request.user
        shop_id = request.data.get('shop_id')
        receive_notifications = request.data.get('receive_notifications', True)
        notification_frequency = request.data.get('notification_frequency', 'instant')
        
        if not shop_id:
            return Response({'detail': 'Shop ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        shop = Shop.objects.get(id=shop_id)
        
        if SubscriberShop.objects.filter(user=user, shop=shop).exists():
            return Response({'detail': 'Already subscribed to this shop.'}, status=status.HTTP_400_BAD_REQUEST)
        
        SubscriberShop = SubscriberShop.objects.create(
            user=user,
            shop=shop,
            receive_notifications=receive_notifications,
            notification_frequency=notification_frequency
        )
        
        return Response({'detail': 'Successfully subscribed to the shop.'}, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'], url_path='unsubscribe')
    def unsubscribe(self, request):
        user = request.user
        shop_id = request.data.get('shop_id')
        
        if not shop_id:
            return Response({'detail': 'Shop ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        shop = Shop.objects.get(id=shop_id)
        SubscriberShop = SubscriberShop.objects.filter(user=user, shop=shop)
        
        if not SubscriberShop.exists():
            return Response({'detail': 'Not subscribed to this shop.'}, status=status.HTTP_400_BAD_REQUEST)
        
        SubscriberShop.update(is_active=False)
        return Response({'detail': 'Successfully unsubscribed from the shop.'}, status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['post'], url_path='update-notification-preferences')
    def update_notification_preferences(self, request):
        user = request.user
        shop_id = request.data.get('shop_id')
        receive_notifications = request.data.get('receive_notifications')
        notification_frequency = request.data.get('notification_frequency')

        if not shop_id:
            return Response({'detail': 'Shop ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        SubscriberShop = SubscriberShop.objects.filter(user=user, shop__id=shop_id).first()
        if not SubscriberShop:
            return Response({'detail': 'SubscriberShop not found.'}, status=status.HTTP_404_NOT_FOUND)

        SubscriberShop.receive_notifications = receive_notifications if receive_notifications is not None else SubscriberShop.receive_notifications
        SubscriberShop.notification_frequency = notification_frequency if notification_frequency else SubscriberShop.notification_frequency
        SubscriberShop.save()

        return Response({'detail': 'Notification preferences updated successfully.'}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='my-subscriptions')
    def my_subscriptions(self, request):
        user = request.user
        subscriptions = SubscriberShop.objects.filter(user=user, is_active=True)
        serializer = self.get_serializer(subscriptions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'], url_path='subscribers')
    def get_subscribers(self, request, pk=None):
        shop = self.get_object()
        subscribers = SubscriberShop.objects.filter(shop=shop, is_active=True)
        serializer = self.get_serializer(subscribers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
