from django.urls import path, include
from rest_framework.routers import DefaultRouter
from shop.views.subscription import CheckSubscriptionStatusView, SubscriptionViewSet, SubscriptionHistoryViewSet

router = DefaultRouter()
router.register(r'subscriptions', SubscriptionViewSet)
router.register(r'subscription-history', SubscriptionHistoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('check-subscription-status/', CheckSubscriptionStatusView.as_view(), name='check_subscription_status'),
]
