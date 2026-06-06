"""
Serializers para autenticación: login, OTP, registro.
"""
from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from django.utils.crypto import constant_time_compare

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
            )
        except OTPToken.DoesNotExist:
            raise serializers.ValidationError("Código OTP inválido.")

        if not otp.is_valid:
            raise serializers.ValidationError("Código OTP expirado o ya utilizado.")

        code_is_valid = (
            check_password(data['otp_code'], otp.code_hash)
            if otp.code_hash
            else constant_time_compare(otp.code, data['otp_code'])
        )
        if not code_is_valid:
            raise serializers.ValidationError("Código OTP inválido.")

        data['otp'] = otp
        data['user'] = otp.user
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    """Información del usuario autenticado."""
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                  'role', 'is_2fa_enabled', 'last_login', 'created_at']
        read_only_fields = fields

    def get_role(self, obj):
        return obj.effective_role
