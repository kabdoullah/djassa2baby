from django.urls import path, include
from rest_framework.routers import DefaultRouter
from shop.views.product import CategoryViewSet, ProductViewSet, ImageViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'images', ImageViewSet, basename='image')

urlpatterns = [
    path('', include(router.urls)),
]