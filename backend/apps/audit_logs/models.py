"""
Modelo AuditLog: registra todos los eventos de seguridad y uso del sistema.
"""
import uuid
from django.db import models
from django.conf import settings


class AuditLog(models.Model):
    """
    Registro de auditoría completo del sistema.
    Alineado con principios ISO 27001 para trazabilidad y no repudio.
    """

    class Action(models.TextChoices):
        # Autenticación
        LOGIN_SUCCESS = 'LOGIN_SUCCESS', 'Inicio de sesión exitoso'
        LOGIN_FAILED = 'LOGIN_FAILED', 'Inicio de sesión fallido'
        LOGIN_OTP_SENT = 'LOGIN_OTP_SENT', 'OTP enviado'
        LOGOUT = 'LOGOUT', 'Cierre de sesión'
        ACCOUNT_LOCKED = 'ACCOUNT_LOCKED', 'Cuenta bloqueada'

        # Chatbot
        CHAT_QUERY = 'CHAT_QUERY', 'Consulta al chatbot'
        CHAT_VOICE_QUERY = 'CHAT_VOICE_QUERY', 'Consulta de voz al chatbot'

        # Datos académicos
        DATA_ACCESS_GRADES = 'DATA_ACCESS_GRADES', 'Acceso a notas'
        DATA_ACCESS_SCHEDULE = 'DATA_ACCESS_SCHEDULE', 'Acceso a horarios'
        DATA_ACCESS_PROFILE = 'DATA_ACCESS_PROFILE', 'Acceso a perfil académico'
        DATA_ACCESS_STATS = 'DATA_ACCESS_STATS', 'Acceso a estadísticas académicas'
        DATA_ACCESS_ACTIVITIES = 'DATA_ACCESS_ACTIVITIES', 'Acceso a actividades'
        DATA_ACCESS_NOTIFICATIONS = 'DATA_ACCESS_NOTIFICATIONS', 'Acceso a notificaciones'
        DATA_SUBMIT_ACTIVITY = 'DATA_SUBMIT_ACTIVITY', 'Entrega de actividad'
        TEACHER_CREATE_ACTIVITY = 'TEACHER_CREATE_ACTIVITY', 'Creación de actividad docente'

        # RAG
        RAG_QUERY = 'RAG_QUERY', 'Consulta al índice RAG'
        RAG_INDEX_BUILD = 'RAG_INDEX_BUILD', 'Construcción del índice RAG'

        # Sistema
        SYSTEM_ERROR = 'SYSTEM_ERROR', 'Error del sistema'

    class Severity(models.TextChoices):
        INFO = 'INFO', 'Información'
        WARNING = 'WARNING', 'Advertencia'
        CRITICAL = 'CRITICAL', 'Crítico'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='audit_logs',
        help_text="Usuario que realizó la acción (null si anónimo)"
    )
    action = models.CharField(max_length=50, choices=Action.choices)
    severity = models.CharField(
        max_length=10,
        choices=Severity.choices,
        default=Severity.INFO
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, default='')
    metadata = models.JSONField(default=dict, blank=True,
                                help_text="Datos adicionales del evento (JSON)")
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = 'audit_log'
        verbose_name = 'Log de Auditoría'
        verbose_name_plural = 'Logs de Auditoría'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['action', 'timestamp']),
            models.Index(fields=['severity', 'timestamp']),
        ]

    def __str__(self):
        user_str = self.user.username if self.user else 'Anónimo'
        return f"[{self.severity}] {self.action} — {user_str} — {self.timestamp}"
