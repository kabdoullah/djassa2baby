from django.urls import path
from .views import CreateUserView, CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from .views import PasswordResetView, PasswordResetConfirmView, PasswordChangeView

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create_user'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-change/', PasswordChangeView.as_view(), name='password_change'),
]
