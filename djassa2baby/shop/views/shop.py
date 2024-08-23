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
from users.models import User


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


    @action(detail=False, methods=['POST'], url_path='create-shop-with-owner', url_name='create-shop-with-owner')
    def create_shop_with_owner(self, request):

        """
        Crée une nouvelle boutique.

        Cette méthode permet de créer une nouvelle instance de Shop en utilisant les données fournies dans la requête.
        Elle valide les données à l'aide du ShopSerializer avant de sauvegarder la nouvelle boutique dans la base de données.

        Args:
            request (Request): L'objet de la requête HTTP contenant les données pour créer une nouvelle boutique.

        Returns:
            Response: Un objet Response contenant les données de la nouvelle boutique créée.

        Status Codes:
            201 Created: Si la boutique est créée avec succès.
            400 Bad Request: Si les données fournies sont invalides.
        """

        
        data = request.data.copy()  # Create a copy of the request data to modify it

        # Récupérer le numéro de téléphone et le mot de passe pour créer un compte utilisateur pour le propriétaire de la boutique
        username = data.get('phone_number_1')
        password = data.get('password')

        # Vérifier si le numéro de téléphone et le mot de passe sont fournis
        if not username or not password:
            return Response({"error": "Le numéro de téléphone et le mot de passe sont obligatoires."}, status=status.HTTP_400_BAD_REQUEST)

        # Créer le compte utilisateur pour le propriétaire de la boutique
        user = User.objects.create_user(username=username, password=password, email=data.get('email '))
        
        # Supprimer les clés phone_number_1 et password avant de créer la boutique
        data.pop('phone_number_1', None)
        data.pop('password', None)

        # Ajouter l'ID de l'utilisateur à la donnée pour créer la boutique
        data['user'] = user.id

        # Valider et enregistrer la boutique
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        """
        Effectue la sauvegarde de la nouvelle boutique dans la base de données.
        
        Cette méthode peut être surchargée pour personnaliser la façon dont les boutiques sont créées et sauvegardées.

        Args:
            serializer (Serializer): L'instance du serializer contenant les données validées.
        """
        serializer.save()




class ShopReviewViewSet(viewsets.ModelViewSet):
    queryset = ShopReview.objects.all()
    serializer_class = ShopReviewSerializer
    permission_classes = [UnauthenticatedReadonly]
