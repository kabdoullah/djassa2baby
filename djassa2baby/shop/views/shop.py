from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.shortcuts import get_object_or_404
from shop.permissions.permission import UnauthenticatedReadonly
from rest_framework.parsers import MultiPartParser, FormParser
from shop.models.shop import Shop, ShopReview
from shop.serializers.shop import ShopSerializer, ShopReviewSerializer, ShopOwnerSerializer
from shop.serializers.product import ProductResponseSerializer
from shop.models.product import Category
from users.models import User, Role

class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [UnauthenticatedReadonly]
    lookup_field = 'slug'

    def get_queryset(self):
        return Shop.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

    @action(detail=False, methods=['GET'], url_path="products/category/(?P<category_slug>[^/.]+)",
            url_name="products_by_category")

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

        Return:
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


from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

class CreateShopWithOwnerAPIView(APIView):
    
    """
    API view to create a new shop along with the shop owner.
    """

    # permission_classes = [UnauthenticatedReadonly]
    serializer_class = ShopOwnerSerializer
    @swagger_auto_schema(request_body=ShopOwnerSerializer, responses={201: ShopOwnerSerializer})
    def post(self, request, *args, **kwargs):

        """
        Handles POST request to create shop with owner.
        
        Args:
            request (Request): The HTTP request object containing the data to create a new shop and owner.
        
        Returns:
            Response: A Response object containing the data of the newly created shop and owner.
        
        Status Codes:
            201 Created: If the shop and owner are successfully created.
            400 Bad Request: If the provided data is invalid.
        """

        data = request.data  # Create a copy of the request data to modify it
        # Récupérer le numéro de téléphone et le mot de passe pour créer un compte utilisateur pour le propriétaire de la boutique
        username = data.get('phone_number_1')
        password = data.get('password')
        # Vérifier si le numéro de téléphone et le mot de passe sont fournis
        if not username or not password:
            return Response({"error": "Le numéro de téléphone et le mot de passe sont obligatoires."}, status=status.HTTP_400_BAD_REQUEST)

        # Use ShopOwnerSerializer to validate and process the modified data
        serializer = ShopOwnerSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    
