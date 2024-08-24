from django.urls import path, include
from rest_framework.routers import DefaultRouter
from shop.views.subscriber import SubscriberShopViewSet
router = DefaultRouter()
router.register(r'subscribers', SubscriberShopViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

