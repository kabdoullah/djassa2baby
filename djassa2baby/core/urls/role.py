from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views.role import RoleViewSet

router = DefaultRouter()
router.register(r'roles', RoleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
