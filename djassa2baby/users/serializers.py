from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, max_length=20, min_length=6)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email',
                  'phone_number', 'role', 'is_active', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
