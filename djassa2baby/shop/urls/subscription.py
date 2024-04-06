from django.urls import path, include
from rest_framework.routers import DefaultRouter
from shop.views.subscription import SubscriptionViewSet, SubscriptionHistoryViewSet

router = DefaultRouter()
router.register(r'subscriptions', SubscriptionViewSet)
router.register(r'subscription-history', SubscriptionHistoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
