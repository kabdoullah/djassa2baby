from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.shortcuts import get_object_or_404
from shop.permissions.permission import UnauthenticatedReadonly
from rest_framework.parsers import MultiPartParser, FormParser
from shop.models.shop import Shop, ShopReview
from shop.serializers.shop import ShopSerializer, ShopReviewSerializer
from shop.serializers.product import ProductResponseSerializer
from shop.models.product import Category



class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [UnauthenticatedReadonly]
    lookup_field = 'slug'

    def get_queryset(self):
        return Shop.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['GET'], url_path="products", url_name="products")
    def list_products(self, request, slug=None):
        shop = self.get_object()
        products = shop.products.all()
        serializer = ProductResponseSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['GET'], url_path="products/category/(?P<category_slug>[^/.]+)", url_name="products_by_category")
    def list_products_by_category(self, request, category_slug=None, slug=None):
        try:
            category = Category.objects.get(slug=category_slug)
            products = category.products.all()
            serializer = ProductResponseSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({"error": "Category not found in this shop"}, status=status.HTTP_404_NOT_FOUND)


class ShopReviewViewSet(viewsets.ModelViewSet):
    queryset = ShopReview.objects.all()
    serializer_class = ShopReviewSerializer
    permission_classes = [UnauthenticatedReadonly]
