from rest_framework import viewsets
from core.models.role import Role
from core.serializers.role import RoleSerializer

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
