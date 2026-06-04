"""
Modelo de usuario personalizado con soporte para JWT + 2FA.
Extiende AbstractBaseUser para máximo control sobre autenticación.
"""
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """Usuario extendido con campos para 2FA y seguridad."""

    class Role(models.TextChoices):
        STUDENT = 'student', 'Estudiante'
        TEACHER = 'teacher', 'Docente'
        ADMIN = 'admin', 'Administrador'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, help_text="Correo institucional @pucesi.edu.ec")
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)

    # 2FA
    is_2fa_enabled = models.BooleanField(default=True)
    otp_secret = models.CharField(max_length=32, blank=True, default='')

    # Seguridad
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    failed_login_attempts = models.PositiveSmallIntegerField(default=0)
    account_locked_until = models.DateTimeField(null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    class Meta:
        db_table = 'auth_user'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f"{self.username} ({self.email})"

    @property
    def is_locked(self):
        """Verifica si la cuenta está bloqueada por intentos fallidos."""
        if self.account_locked_until and self.account_locked_until > timezone.now():
            return True
        return False

    def increment_failed_attempts(self):
        """Incrementa intentos fallidos y bloquea si supera el límite."""
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= 5:
            self.account_locked_until = timezone.now() + timezone.timedelta(minutes=15)
        self.save(update_fields=['failed_login_attempts', 'account_locked_until'])

    def reset_failed_attempts(self):
        """Resetea el contador de intentos fallidos tras login exitoso."""
        self.failed_login_attempts = 0
        self.account_locked_until = None
        self.save(update_fields=['failed_login_attempts', 'account_locked_until'])

    @property
    def effective_role(self):
        if self.is_staff or self.is_superuser:
            return self.Role.ADMIN
        return self.role

    @property
    def is_teacher(self):
        return self.effective_role == self.Role.TEACHER


class OTPToken(models.Model):
    """Token OTP temporal para 2FA. Expira en 5 minutos."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otp_tokens')
    code = models.CharField(max_length=6)
    temp_token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    class Meta:
        db_table = 'auth_otp_token'
        verbose_name = 'Token OTP'
        ordering = ['-created_at']

    def __str__(self):
        return f"OTP:{self.code} para {self.user.username} (expira: {self.expires_at})"

    @property
    def is_valid(self):
        """Verifica si el OTP es válido (no expirado, no usado)."""
        return not self.is_used and self.expires_at > timezone.now()
