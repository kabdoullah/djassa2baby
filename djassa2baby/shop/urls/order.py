from django.urls import path, include
from rest_framework.routers import DefaultRouter
from shop.views.order import OrderViewSet, CreateAnonymousOrderView

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'anonymous-orders', CreateAnonymousOrderView, basename='anonymous-order')


urlpatterns = [
    path('', include(router.urls)),
]
