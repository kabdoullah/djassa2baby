from django.urls import path

from shop.views.otp import VerifyOtpAPIView, ResendOtpAPIView

urlpatterns = [
    path('verify-otp/', VerifyOtpAPIView.as_view(), name='verify-otp'),
    path('resend-otp/', ResendOtpAPIView.as_view(), name='resend-otp'),
]
