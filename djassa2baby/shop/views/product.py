from rest_framework import viewsets
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.decorators import action
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
        serializer = ProductResponseSerializer(
            queryset, many=True, context=self.get_serializer_context())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ProductResponseSerializer(
            instance, context=self.get_serializer_context())
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], url_path='category/(?P<category_slug>[^/.]+)', url_name='filter_by_category')
    def filter_by_category(self, request, category_slug=None):
        try:
            category = Category.objects.get(slug=category_slug)
            products = Product.objects.filter(category=category)
            serializer = ProductResponseSerializer(
                products, many=True, context=self.get_serializer_context())
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['GET'], url_path='reviews', url_name='product_reviews')
    def list_reviews(self, request, slug=None):
        product = self.get_object()
        reviews = product.reviews.all()
        serializer = ProductReviewSerializer(reviews, many=True)
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
    """
    A simple ViewSet for listing similar products.

    This ViewSet provides an endpoint to retrieve products that are similar to
    a given product or belong to a specific category. The similarity criteria
    can be customized as needed.
    """

    serializer_class = ProductResponseSerializer

    def list(self, request):
        """
        List similar products based on category or product.

        This method retrieves a list of products that are similar to the product specified
        by the `product_id` query parameter, or products that belong to the same category
        as specified by the `category_id` query parameter.

        Query Parameters:
        - category_id: The ID of the category to find similar products.
        - product_id: The ID of the product to find similar products.

        Returns:
        - A list of similar products serialized using `ProductResponseSerializer`.
        """
        category_id = request.query_params.get('category_id')
        product_id = request.query_params.get('product_id')

        if category_id:
            # Retrieve products from the same category, excluding the specified product
            products = Product.objects.filter(
                category_id=category_id).exclude(id=product_id)[:5]
        elif product_id:
            # Retrieve similar products based on the specified product's category
            product = Product.objects.get(id=product_id)
            products = Product.objects.filter(
                category=product.category).exclude(id=product_id)[:5]
        else:
            # Default to retrieving the first 5 products (this can be customized)
            products = Product.objects.all()[:5]

        # Serialize the list of similar products
        serializer = self.serializer_class(products, many=True)
        return Response(serializer.data)
