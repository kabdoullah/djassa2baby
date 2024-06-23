from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, PasswordResetSerializer, PasswordResetConfirmSerializer, PasswordChangeSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from shop.serializers.shop import ShopSerializer
from shop.models.shop import Shop
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from users.models import User
from .utils import Util


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
            shop = Shop.objects.filter(user=user).first()
            if shop:
                response_data['shop'] = ShopSerializer(shop).data

        return Response(response_data, status=status.HTTP_200_OK)


class PasswordResetView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data['email']
            user = User.objects.filter(email=email).first()
            if user:
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_url = f'{settings.FRONTEND_URL}/reset-password/{uid}/{token}/'
                Util.send_mail(
                    'Password Reset',
                    f'Use the link below to reset your password:\n{reset_url}',
                    settings.DEFAULT_FROM_EMAIL,
                    [email]
                )
            return Response({"message": "If the email is registered, you will receive a reset link."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            uid = force_str(urlsafe_base64_decode(
                serializer.data['token'].split('-')[0]))
            token = serializer.data['token'].split('-')[1]
            new_password = serializer.data['new_password']
            user = User.objects.filter(pk=uid).first()
            if user and default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid token or user."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordChangeView(generics.UpdateAPIView):
    serializer_class = PasswordChangeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            old_password = serializer.data['old_password']
            new_password = serializer.data['new_password']
            if not user.check_password(old_password):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(new_password)
            user.save()
            return Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
