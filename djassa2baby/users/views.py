from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import CustomUserSerializer


class CreateUserView(CreateAPIView):
    serializer_class = CustomUserSerializer

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({'user': serializer.data, 'refresh': str(refresh), 'access': str(refresh.access_token)}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
