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
        serializer = ProductResponseSerializer(products, many=True, context=self.get_serializer_context())
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request):
        query = request.query_params.get('q', None)
        if query:
            shops = Shop.objects.filter(name__icontains=query)
            serializer = self.get_serializer(shops, many=True)
            return Response(serializer.data)
        return Response({'error': 'No query provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    
    @action(detail=False, methods=['GET'], url_path="products/category/(?P<category_slug>[^/.]+)", url_name="products_by_category")
    def list_products_by_category(self, request, category_slug=None, slug=None):
        try:
            category = Category.objects.get(slug=category_slug)
            products = category.products.all()
            serializer = ProductResponseSerializer(products, many=True, context=self.get_serializer_context())
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({"error": "Category not found in this shop"}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request):
        """
        Recherchez des boutiques en fonction d'un terme de requête.

        Cette méthode permet de rechercher des boutiques dont le nom contient le terme de recherche fourni dans les paramètres de requête. Elle filtre les résultats en utilisant une recherche insensible à la casse (case-insensitive) sur le nom des boutiques.

        Args:
            request (Request): L'objet de la requête HTTP contenant les paramètres de requête.

        Query Parameters:
            q (str): Le terme de recherche utilisé pour filtrer les boutiques par nom.

        Returns:
            Response: Un objet Response contenant les boutiques correspondant au terme de recherche. 
                    En cas d'absence de terme de recherche, retourne une réponse avec un message d'erreur et un code de statut HTTP 400 Bad Request.
                    
        Status Codes:
            200 OK: Si des boutiques sont trouvées et retournées avec succès.
            400 Bad Request: Si aucun terme de recherche n'est fourni.
        """
        query = request.query_params.get('q', None)
        if query:
            shops = Shop.objects.filter(name__icontains=query)
            serializer = self.get_serializer(shops, many=True)
            return Response(serializer.data)
        return Response({'error': 'No query provided'}, status=status.HTTP_400_BAD_REQUEST)



class ShopReviewViewSet(viewsets.ModelViewSet):
    queryset = ShopReview.objects.all()
    serializer_class = ShopReviewSerializer
    permission_classes = [UnauthenticatedReadonly]
