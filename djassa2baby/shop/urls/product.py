from django.urls import path, include
from rest_framework.routers import DefaultRouter
from shop.views.product import CategoryViewSet, ProductViewSet, ProductReviewViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'product-reviews', ProductReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]