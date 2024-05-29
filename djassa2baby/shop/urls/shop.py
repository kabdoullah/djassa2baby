from django.urls import path, include
from rest_framework.routers import DefaultRouter
from shop.views.shop import ShopViewSet, ShopReviewViewSet


router = DefaultRouter()
router.register(r'shops', ShopViewSet, basename='shop')
router.register(r'shop-reviews', ShopReviewViewSet, basename='shop-review')

urlpatterns = [
    path('', include(router.urls)),
]
