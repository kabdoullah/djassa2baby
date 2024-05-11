from rest_framework import viewsets
from shop.permissions.permission import UnauthenticatedReadonly
from rest_framework.parsers import MultiPartParser, FormParser
from shop.models.shop import Shop, ShopReview
from shop.serializers.shop import ShopSerializer, ShopReviewSerializer


class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [UnauthenticatedReadonly]


class ShopReviewViewSet(viewsets.ModelViewSet):
    queryset = ShopReview.objects.all()
    serializer_class = ShopReviewSerializer
    permission_classes = [UnauthenticatedReadonly]
