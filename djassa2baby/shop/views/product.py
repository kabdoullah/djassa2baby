from rest_framework import viewsets
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from shop.permissions.permission import UnauthenticatedReadonly
from rest_framework.parsers import MultiPartParser, FormParser
from shop.models.product import Product, Category, ProductReview
from shop.serializers.product import ProductSerializer, CategorySerializer, ProductReviewSerializer, ProductResponseSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [UnauthenticatedReadonly]
    parser_classes = [MultiPartParser, FormParser]
    lookup_field = 'slug'

    def list(self, request, *args, **kwargs):
        queryset = Product.objects.all()
        serializer = ProductResponseSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ProductResponseSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [UnauthenticatedReadonly]
    parser_classes = [MultiPartParser, FormParser]
    lookup_field = 'slug'

    def get_queryset(self):
        return Category.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductReviewViewSet(viewsets.ModelViewSet):
    queryset = ProductReview.objects.all()
    serializer_class = ProductReviewSerializer
    permission_classes = [UnauthenticatedReadonly]


class SimilarProductsViewSet(viewsets.ViewSet):
    serializer_class = ProductResponseSerializer

    def list(self, request):
        category_id = request.query_params.get('category_id')
        product_id = request.query_params.get('product_id')

        if category_id:
            # Récupérer les produits de la même catégorie (à l'exclusion du produit lui-même)
            products = Product.objects.filter(
                category_id=category_id).exclude(id=product_id)[:5]
        elif product_id:
            # Récupérer les produits similaires (à adapter selon vos critères)
            product = Product.objects.get(id=product_id)
            products = Product.objects.filter(
                category=product.category).exclude(id=product_id)[:5]
        else:
            # Ajustez pour d'autres critères de similarité
            products = Product.objects.all()[:5]

        serializer = self.serializer_class(products, many=True)
        return Response(serializer.data)
