from django.urls import path

from shop.views.otp import VerifyOtpAPIView

urlpatterns = [
    path('verify-otp/', VerifyOtpAPIView.as_view(), name='verify-otp'),
]
