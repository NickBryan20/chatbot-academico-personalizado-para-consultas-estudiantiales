"""
Servicio de Auditoría: interfaz centralizada para registrar eventos.
Todos los módulos del sistema llaman a este servicio.
"""
import logging
from typing import Optional

from .models import AuditLog

logger = logging.getLogger(__name__)


class AuditLogService:
    """Servicio centralizado de registro de auditoría."""

    @staticmethod
    def log(
        action: str,
        user=None,
        request=None,
        metadata: Optional[dict] = None,
        severity: str = AuditLog.Severity.INFO,
    ) -> AuditLog:
        """
        Registra un evento en el audit log.

        Args:
            action: Código de acción (de AuditLog.Action)
            user: Usuario que realizó la acción (puede ser None)
            request: Request HTTP (para extraer IP y user agent)
            metadata: Datos adicionales del evento
            severity: Nivel de severidad
        """
        ip_address = None
        user_agent = ''

        if request:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            ip_address = (
                x_forwarded_for.split(',')[0].strip()
                if x_forwarded_for
                else request.META.get('REMOTE_ADDR')
            )
            user_agent = request.META.get('HTTP_USER_AGENT', '')

        try:
            log_entry = AuditLog.objects.create(
                user=user,
                action=action,
                severity=severity,
                ip_address=ip_address,
                user_agent=user_agent,
                metadata=metadata or {},
            )
            logger.debug(f"AuditLog: [{severity}] {action} — user={getattr(user, 'username', 'anon')}")
            return log_entry
        except Exception as e:
            # El logging nunca debe romper el flujo principal
            logger.error(f"Error registrando audit log: {e}")

    @classmethod
    def log_login_failed(cls, user, reason: str = "unknown", request=None):
        return cls.log(
            action=AuditLog.Action.LOGIN_FAILED,
            user=user,
            request=request,
            severity=AuditLog.Severity.WARNING,
            metadata={
                'reason': reason,
                'failed_attempts': getattr(user, 'failed_login_attempts', 0),
            }
        )

    @classmethod
    def log_chat_query(cls, user, query: str, response_preview: str, tokens_used: int, request=None):
        return cls.log(
            action=AuditLog.Action.CHAT_QUERY,
            user=user,
            request=request,
            metadata={
                'query_preview': query[:100],
                'response_preview': response_preview[:100],
                'tokens_used': tokens_used,
            }
        )

    @classmethod
    def log_data_access(cls, user, data_type: str, request=None):
        action_map = {
            'grades': AuditLog.Action.DATA_ACCESS_GRADES,
            'schedule': AuditLog.Action.DATA_ACCESS_SCHEDULE,
            'profile': AuditLog.Action.DATA_ACCESS_PROFILE,
        }
        action = action_map.get(data_type, AuditLog.Action.DATA_ACCESS_PROFILE)
        return cls.log(action=action, user=user, request=request)
