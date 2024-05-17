from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from shop.permissions.permission import UnauthenticatedReadonly
from rest_framework.parsers import MultiPartParser, FormParser
from shop.models.shop import Shop, ShopReview
from shop.serializers.shop import ShopSerializer, ShopReviewSerializer


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


class ShopReviewViewSet(viewsets.ModelViewSet):
    queryset = ShopReview.objects.all()
    serializer_class = ShopReviewSerializer
    permission_classes = [UnauthenticatedReadonly]
