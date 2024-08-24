from rest_framework import viewsets,status
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets # type: ignore
from core.models.coupon import Coupon
from core.serializers.coupon import CouponSerializer
from djassa2baby.shop.models.order import Order
from rest_framework.decorators import action
from rest_framework.response import Response

from djassa2baby.shop.permissions.permission import IsClient, IsSeller, UnauthenticatedReadonly


class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    # permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'delete', 'update']:
            self.permission_classes = [IsAuthenticated, IsSeller]
        elif self.action == 'get_coupon_details':
            self.permission_classes = [UnauthenticatedReadonly]
        elif self.action == 'get_publish_coupon':
            self.permission_classes = [UnauthenticatedReadonly]
        else:
            self.permission_classes = [IsAuthenticated]
        return super(CouponViewSet, self).get_permissions()
    

    @action(detail=False, methods=['get'], url_path='coupon-details/(?P<coupon_code>[^/.]+)')
    def get_coupon_details(self, request, coupon_code=None):
        try:
            coupon = Coupon.objects.get(coupon_code = coupon_code)
        except Coupon.DoesNotExist:
            return Response({'detail': 'Coupon not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(coupon)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='publish-coupons/(?P<shop_id>[^/.]+)')
    def get_publish_coupon(self, request, shop_id=None):
        '''
            Return the published coupons for the shop in request (shop_id)
        '''
        try:
            # Filter coupons by shop and ensure they are published
            coupons = Coupon.objects.filter(shop=shop_id, is_publish=True)
        except Coupon.DoesNotExist:
            return Response({'detail': 'Coupon not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Serialize the filtered coupons
        serializer = self.get_serializer(coupons, many=True)
        return Response(serializer.data)

