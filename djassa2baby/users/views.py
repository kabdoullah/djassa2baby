from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from shop.serializers.shop import ShopSerializer


class CreateUserView(CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({'user': serializer.data, 'refresh': str(refresh), 'access': str(refresh.access_token)}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Obtenir les tokens d'authentification
        tokens = serializer.validated_data
        refresh = tokens.get('refresh')
        access = tokens.get('access')

        # Obtenir l'utilisateur authentifié
        user = serializer.user

        # Construire les données de réponse
        response_data = {
            'refresh': str(refresh),
            'access': str(access),
            'user': UserSerializer(user).data
        }

       
        if user.role and user.role.label == 'vendeur':
            shop = user.shop  
            if shop:
                response_data['shop'] = ShopSerializer(shop).data

        
        return Response(response_data, status=status.HTTP_200_OK)
