from rest_framework import serializers
from shop.models.otp import OtpCode

class OtpVerificationSerializer(serializers.Serializer):

    shop_id = serializers.UUIDField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        shop_id = data.get('shop_id')
        otp_code = data.get('otp')

        try:
            otp_instance = OtpCode.objects.get(shop=shop_id, otp=otp_code)
        except OtpCode.DoesNotExist:
            raise serializers.ValidationError("OTP invalide ou introuvable.")

        if otp_instance.has_expired():
            raise serializers.ValidationError("Le code OTP a expiré.")

        if not otp_instance.is_active:
            raise serializers.ValidationError("Le code OTP a déjà été utilisé.")

        return data
