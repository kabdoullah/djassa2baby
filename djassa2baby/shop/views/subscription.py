from rest_framework import viewsets
from rest_framework import permissions
from shop.models.shop import Shop
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


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.utils.timezone import now
from datetime import timedelta


class CheckSubscriptionStatusView(APIView):

    """
        APi to check if the store are in free month plan 
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        shop = Shop.objects.filter(user=user).first()

        if not shop:
            return Response({"detail": "Shop not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user is within the one-month free period
        one_month_after_registration = shop.date_added + timedelta(days=30)
        if now() <= one_month_after_registration:
            return Response({"status": "active", "message": "You are within the free subscription period."}, status=status.HTTP_200_OK)

        # After the free period, check if the user has paid for the current month
        last_payment = SubscriptionHistory.objects.filter(shop=shop).order_by('-payment_date').first()

        if last_payment:
            next_due_date = last_payment.payment_date + timedelta(days=30)
            if now() > next_due_date:
                return Response({"status": "expired", "message": "Your subscription has expired. Please renew."}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({"status": "active", "message": "Your subscription is active."}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "expired", "message": "No payment history found. Please subscribe."}, status=status.HTTP_403_FORBIDDEN)
