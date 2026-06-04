"""Controladores de negocio para el módulo de Autenticación."""
import logging
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from ..audit_logs.services import AuditLogService
from .services import OTPService

logger = logging.getLogger(__name__)

def get_client_ip(request):
    """Obtiene la IP real del cliente (considera proxy)."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')

class AuthenticationController:
    @staticmethod
    def process_direct_login(user, request):
        """Lógica de negocio para login directo (sin 2FA)."""
        user.reset_failed_attempts()
        user.last_login_ip = get_client_ip(request)
        user.last_login = timezone.now()
        user.save(update_fields=['last_login_ip', 'last_login'])

        refresh = RefreshToken.for_user(user)
        
        AuditLogService.log(
            user=user,
            action='LOGIN_SUCCESS',
            request=request,
            metadata={'method': 'Direct Password (2FA disabled)'}
        )
        logger.info(f"Login exitoso para {user.username} (Directo). Tokens emitidos.")
        
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }

    @staticmethod
    def process_otp_login(user, otp_code, request):
        """Lógica de negocio para login con 2FA."""
        OTPService.mark_used(otp_code)
        user.reset_failed_attempts()
        
        user.last_login_ip = get_client_ip(request)
        user.last_login = timezone.now()
        user.save(update_fields=['last_login_ip', 'last_login'])

        refresh = RefreshToken.for_user(user)
        
        AuditLogService.log(
            user=user,
            action='LOGIN_SUCCESS',
            request=request,
            metadata={'method': '2FA+OTP'}
        )
        logger.info(f"Login completo para {user.username}. Tokens emitidos.")
        
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }

    @staticmethod
    def process_logout(user, refresh_token, request):
        """Lógica de negocio para invalidar sesión."""
        if not refresh_token:
            raise ValueError("Proporciona el refresh token.")
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            AuditLogService.log(user=user, action='LOGOUT', request=request)
        except TokenError as e:
            raise ValueError("Token inválido.") from e
