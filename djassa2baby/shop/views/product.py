from shop.models.shop import Shop
from rest_framework import viewsets
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from shop.permissions.permission import UnauthenticatedReadonly
from rest_framework.parsers import MultiPartParser, FormParser
from shop.models.product import Product, Category, ProductReview, ShopCategorie
from shop.serializers.product import (ProductSerializer,
                                      CategorySerializer,
                                      ProductReviewSerializer,
                                      ProductResponseSerializer,
                                      ProductReviewCreateSerializer, ShopCategorieSerializer
                                      )


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

    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request):
        """
        Recherchez des produits en fonction d'un terme de requête.

        Cette méthode permet de rechercher des produits dont le nom contient le terme de recherche fourni dans les paramètres de requête. Elle filtre les résultats en utilisant une recherche insensible à la casse (case-insensitive) sur le nom des boutiques.

        Args:
            request (Request): L'objet de la requête HTTP contenant les paramètres de requête.

        Query Parameters:
            q (str): Le terme de recherche utilisé pour filtrer les produits par nom.

        Returns:
            Response: Un objet Response contenant les produits correspondant au terme de recherche.
                    En cas d'absence de terme de recherche, retourne une réponse avec un message d'erreur et un code de statut HTTP 400 Bad Request.

        Status Codes:
            200 OK: Si des boutiques sont trouvées et retournées avec succès.
            400 Bad Request: Si aucun terme de recherche n'est fourni.
        """
        query = request.query_params.get('q', None)
        if query:
            products = Product.objects.filter(name__icontains=query)
            serializer = self.get_serializer(products, many=True)
            return Response(serializer.data)
        return Response({'error': 'No query provided'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='category/(?P<category_id>[^/.]+)')
    def search_by_category(self, request, category_id=None):
        products = Product.objects.filter(category_id=category_id)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='shop/(?P<shop_id>[^/.]+)')
    def search_by_shop(self, request, shop_id=None):
        products = Product.objects.filter(shop_id=shop_id)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='shop/(?P<shop_id>[^/.]+)/category/(?P<category_id>[^/.]+)')
    def search_by_shop_and_category(self, request, shop_id=None, category_id=None):
        products = Product.objects.filter(
            shop_id=shop_id, category_id=category_id)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='most-ordered')
    def most_ordered(self, request):
        products = Product.objects.annotate(order_count=Count(
            'orderitem')).order_by('-order_count')[:10]
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='similar')
    def similar_products(self, request, slug=None):
        product = Product.objects.get(slug=slug)
        similar_products = Product.objects.filter(
            category=product.category).exclude(slug=product.slug)
        serializer = self.get_serializer(similar_products, many=True)
        return Response(serializer.data)


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
    serializer_class = ProductReviewCreateSerializer
    permission_classes = [UnauthenticatedReadonly]

    def list(self, request, *args, **kwargs):
        queryset = ProductReview.objects.all()
        serializer = ProductReviewSerializer(queryset, many=True, context=self.get_serializer_context())
        return Response(serializer.data, status=status.HTTP_200_OK)


class ShopCategorieViewSet(viewsets.ModelViewSet):
    queryset = ShopCategorie.objects.all()
    serializer_class = ShopCategorieSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        shop_id = self.request.query_params.get('shop_id')
        if shop_id:
            queryset = queryset.filter(shop__id=shop_id)
        return queryset
    

    @action(detail=False, methods=['get'], url_path='list-categorie/(?P<shop_id>[^/.]+)')
    def shop_categorie(self, request, shop_id=None):
        shop_categories = ShopCategorie.objects.filter(shop_id=shop_id)
        serializer = self.get_serializer(shop_categories, many=True)
        return Response(serializer.data)
    
