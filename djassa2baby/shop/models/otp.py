import uuid

from django.db import models
from django.core.exceptions import ValidationError
from shop.models.shop import Shop
from django.utils import timezone

import random


def generate_otp():

    """Génère un code OTP à 6 chiffres."""

    return str(random.randint(100000, 999999))



def validate_otp(value):

    if len(value) != 6:
        raise ValidationError('OTP doit être composé de 6 chiffres.')
    

class OtpCode(models.Model):

    """
        Otp class to verify the account of store 
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    otp = models.CharField(max_length=6, validators=[validate_otp], default=generate_otp)   
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def deactivate(self):
        self.is_active = False
        self.save()

    def has_expired(self):
        if self.expires_at and timezone.now() > self.expires_at:
            return True
        return False
    
    def verify_otp(self, otp_code):
        
        """Verify the OTP code."""

        if self.is_active and not self.has_expired() and self.otp == otp_code:
            self.deactivate()  # Deactivate OTP after successful verification
            return True
        return False
    

    def __str__(self):
        return self.otp