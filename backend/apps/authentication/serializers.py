"""
Serializers para autenticación: login, OTP, registro.
"""
import random
import string
from datetime import timedelta

from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, OTPToken
from apps.audit_logs.services import AuditLogService


class LoginSerializer(serializers.Serializer):
    """Validar credenciales en el paso 1 del login (antes del OTP)."""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        request = self.context.get('request')

        # Buscar usuario por username o código de estudiante
        from apps.students.models import Student
        user = User.objects.filter(username__iexact=username).first()
        
        if not user:
            # Intentar por código de estudiante
            student = Student.objects.filter(student_code__iexact=username).first()
            if student:
                user = student.user
        
        if not user:
            raise serializers.ValidationError("Credenciales inválidas.")

        # Verificar bloqueo
        if user.is_locked:
            AuditLogService.log_login_failed(user, reason="account_locked", request=request)
            raise serializers.ValidationError(
                "Cuenta bloqueada temporalmente. Intente en 15 minutos."
            )

        # Verificar contraseña
        if not user.check_password(password):
            user.increment_failed_attempts()
            AuditLogService.log_login_failed(user, reason="wrong_password", request=request)
            raise serializers.ValidationError("Credenciales inválidas.")

        if not user.is_active:
            raise serializers.ValidationError("Cuenta inactiva. Contacte al administrador.")

        data['user'] = user
        return data


class OTPVerifySerializer(serializers.Serializer):
    """Validar el OTP para completar el login (paso 2)."""
    temp_token = serializers.UUIDField()
    otp_code = serializers.CharField(min_length=6, max_length=6)

    def validate(self, data):
        try:
            otp = OTPToken.objects.get(
                temp_token=data['temp_token'],
                code=data['otp_code'],
            )
        except OTPToken.DoesNotExist:
            raise serializers.ValidationError("Código OTP inválido.")

        if not otp.is_valid:
            raise serializers.ValidationError("Código OTP expirado o ya utilizado.")

        data['otp'] = otp
        data['user'] = otp.user
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    """Información del usuario autenticado."""

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                  'is_2fa_enabled', 'last_login', 'created_at']
        read_only_fields = fields
