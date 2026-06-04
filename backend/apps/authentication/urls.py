"""URLs del módulo de autenticación."""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import LoginView, OTPVerifyView, LogoutView, ProfileView

urlpatterns = [
    path('login/', LoginView.as_view(), name='auth-login'),
    path('verify-otp/', OTPVerifyView.as_view(), name='auth-verify-otp'),
    path('refresh/', TokenRefreshView.as_view(), name='auth-token-refresh'),
    path('logout/', LogoutView.as_view(), name='auth-logout'),
    path('profile/', ProfileView.as_view(), name='auth-profile'),
]
