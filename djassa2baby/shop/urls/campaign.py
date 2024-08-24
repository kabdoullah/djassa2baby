from django.urls import path, include
from rest_framework.routers import DefaultRouter
from shop.views.campaign import CampaignViewSet

# Créez un routeur et enregistrez le viewset
router = DefaultRouter()
router.register(r'campaigns', CampaignViewSet, basename='campaign')

urlpatterns = [
    path('', include(router.urls)),
]
