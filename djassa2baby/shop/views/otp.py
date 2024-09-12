from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from shop.models.otp import OtpCode
from shop.serializers.otp import OtpVerificationSerializer

class VerifyOtpAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = OtpVerificationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            shop_id = serializer.validated_data['shop_id']
            otp_code = serializer.validated_data['otp']
            # Recherche de l'OTP correspondant
            try:
                otp_instance = OtpCode.objects.get(shop_id=shop_id, otp=otp_code)
            except OtpCode.DoesNotExist:
                return Response({"detail": "OTP introuvable ou invalide."}, status=status.HTTP_404_NOT_FOUND)

            # Vérification et désactivation de l'OTP
            if otp_instance.verify_otp(otp_code):
                return Response({"detail": "OTP vérifié avec succès."}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "OTP invalide ou expiré."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
