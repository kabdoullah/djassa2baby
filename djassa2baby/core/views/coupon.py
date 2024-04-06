from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.models.coupon import Coupon
from core.serializers.coupon import CouponSerializer


class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [IsAuthenticated]
