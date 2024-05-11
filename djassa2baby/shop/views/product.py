from rest_framework import viewsets
from shop.permissions.permission import UnauthenticatedReadonly
from rest_framework.parsers import MultiPartParser, FormParser
from shop.models.product import Product, Category, ProductReview
from shop.serializers.product import ProductSerializer, CategorySerializer, ProductReviewSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [UnauthenticatedReadonly]
    parser_classes = [MultiPartParser, FormParser]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [UnauthenticatedReadonly]
    parser_classes = [MultiPartParser, FormParser]


class ProductReviewViewSet(viewsets.ModelViewSet):
    queryset = ProductReview.objects.all()
    serializer_class = ProductReviewSerializer
    permission_classes = [UnauthenticatedReadonly]


