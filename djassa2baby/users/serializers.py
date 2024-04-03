from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, max_length=10, min_length=6, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email',
                  'phone_number', 'role', 'is_active', 'password']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
