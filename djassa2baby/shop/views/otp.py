from datetime import timedelta, timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import random
from shop.models.shop import Shop
from users.utils import send_otp_email
from shop.models.otp import OtpCode
from shop.serializers.otp import OtpVerificationSerializer
from django.utils import timezone

class VerifyOtpAPIView(APIView):

    """
        API view to verify OTP code to the store.
    """
     
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
                shop = Shop.objects.get(id=shop_id)
                shop.is_active = True
                shop.save()

                return Response({"detail": "OTP vérifié avec succès."}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "OTP invalide ou expiré."}, status=status.HTTP_403_FORBIDDEN)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResendOtpAPIView(APIView):
    """
        API view to resend OTP code to the user if the initial code was not received.
    """
    def post(self, request, *args, **kwargs):
        # Deserialize and validate the incoming data
        serializer = OtpVerificationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            shop_id = serializer.validated_data['shop_id']

            # Try to find an existing OTP for the given shop_id
            try:
                # Generate and save a new OTP
                 #create otp to verify the store account 
                 
                shop = Shop.objects.get(id=shop_id)
                new_otp = OtpCode(
                    otp = generate_otp(),
                    shop = shop,
                    expires_at  = timezone.now() + timedelta(minutes=10)
                )

                new_otp.save()
                # Send the new OTP to the user
                send_otp_email(shop, new_otp)  # Implement this function as needed
                return Response({"detail": "Nouveau code OTP envoyé avec succès."}, status=status.HTTP_200_OK)
            
            except OtpCode.DoesNotExist:
                return Response({"detail": "Aucun OTP actif trouvé pour ce magasin."}, status=status.HTTP_404_NOT_FOUND)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


def generate_otp():

    """
        Génère un code OTP à 6 chiffres.
    """
    
    return str(random.randint(100000, 999999))