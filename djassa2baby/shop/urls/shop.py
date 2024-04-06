from django.urls import path, include
from rest_framework.routers import DefaultRouter
from shop.views.shop import ShopViewSet, ShopReviewViewSet


router = DefaultRouter()
router.register(r'shops', ShopViewSet)
router.register(r'shop-reviews', ShopReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
