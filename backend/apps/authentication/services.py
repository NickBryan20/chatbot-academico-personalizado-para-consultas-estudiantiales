"""
Servicio de OTP: generación, envío (consola en dev) y validación.
"""
import string
import logging
import secrets
from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.utils import timezone

from .models import OTPToken

logger = logging.getLogger(__name__)


class OTPService:
    """Maneja la generación y envío de OTP para 2FA."""

    @staticmethod
    def generate_otp(user) -> OTPToken:
        """
        Genera un nuevo OTP para el usuario.
        Invalida OTPs anteriores del mismo usuario.
        """
        # Invalidar OTPs anteriores no usados
        OTPToken.objects.filter(user=user, is_used=False).update(is_used=True)

        # Generar código numérico con RNG criptográfico.
        code = ''.join(secrets.choice(string.digits) for _ in range(settings.OTP_LENGTH))

        # Calcular expiración
        expires_at = timezone.now() + timedelta(seconds=settings.OTP_EXPIRY_SECONDS)

        # Crear token
        otp = OTPToken.objects.create(
            user=user,
            code='*' * settings.OTP_LENGTH,
            code_hash=make_password(code),
            expires_at=expires_at,
        )
        otp._plain_code = code

        logger.info(f"OTP generado para usuario {user.username}")
        return otp

    @staticmethod
    def send_otp_email(user, otp: OTPToken):
        """
        Envía el OTP por correo al usuario.
        En desarrollo: imprime en consola (EMAIL_BACKEND=console).
        En producción: envía email real a @pucesi.edu.ec.
        """
        subject = "PUCESI - Código de verificación (2FA)"
        code = getattr(otp, '_plain_code', otp.code)
        message = f"""
Estimado/a {user.first_name} {user.last_name},

Tu código de verificación para acceder al Sistema Académico PUCESI es:

    ╔══════════════╗
    ║   {code}   ║
    ╚══════════════╝

Este código es válido por 5 minutos.

Si no solicitaste este código, ignora este mensaje y contacta al departamento de sistemas.

Atentamente,
Sistema Académico PUCESI
Pontificia Universidad Católica del Ecuador — Sede Ibarra
        """

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            logger.info(f"OTP enviado a {user.email}")
        except Exception as e:
            logger.error(f"Error enviando OTP a {user.email}: {e}")
            raise

    @classmethod
    def generate_and_send(cls, user) -> OTPToken:
        """Genera y envía el OTP. Retorna el token creado."""
        otp = cls.generate_otp(user)
        cls.send_otp_email(user, otp)
        return otp

    @staticmethod
    def mark_used(otp: OTPToken):
        """Marca el OTP como usado."""
        otp.is_used = True
        otp.save(update_fields=['is_used'])
