from rest_framework import viewsets
from rest_framework import permissions
from shop.permissions.permission import UnauthenticatedReadonly
from shop.models.subscription import Subscription, SubscriptionHistory
from shop.serializers.subscription import SubscriptionSerializer, SubscriptionHistorySerializer


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    # permission_classes = [UnauthenticatedReadonly]


class SubscriptionHistoryViewSet(viewsets.ModelViewSet):
    queryset = SubscriptionHistory.objects.all()
    serializer_class = SubscriptionHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
