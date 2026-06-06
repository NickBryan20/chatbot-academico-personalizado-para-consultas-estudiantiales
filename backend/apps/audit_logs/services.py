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
    def _request_metadata(request) -> dict:
        if not request:
            return {}

        params = getattr(request, 'query_params', getattr(request, 'GET', {}))
        query_params = {}
        for key in params:
            if hasattr(params, 'getlist'):
                values = params.getlist(key)
                query_params[key] = values if len(values) > 1 else params.get(key)
            else:
                query_params[key] = params.get(key)

        metadata = {
            'http_method': request.method,
            'path': request.path,
        }
        if query_params:
            metadata['query_params'] = query_params

        resolver_match = getattr(request, 'resolver_match', None)
        if resolver_match:
            metadata['view_name'] = resolver_match.view_name
            metadata['url_name'] = resolver_match.url_name

        return metadata

    @staticmethod
    def _actor_metadata(user) -> dict:
        if not user:
            return {}

        return {
            'actor': {
                'id': str(getattr(user, 'id', '')),
                'username': getattr(user, 'username', ''),
                'role': getattr(user, 'role', ''),
                'is_staff': getattr(user, 'is_staff', False),
                'is_superuser': getattr(user, 'is_superuser', False),
            }
        }

    @classmethod
    def log(
        cls,
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

        event_metadata = {}
        event_metadata.update(cls._request_metadata(request))
        event_metadata.update(cls._actor_metadata(user))
        event_metadata.update(metadata or {})

        try:
            log_entry = AuditLog.objects.create(
                user=user,
                action=action,
                severity=severity,
                ip_address=ip_address,
                user_agent=user_agent,
                metadata=event_metadata,
            )
            logger.debug(f"AuditLog: [{severity}] {action} — user={getattr(user, 'username', 'anon')}")
            return log_entry
        except Exception as e:
            # El logging nunca debe romper el flujo principal
            logger.error(f"Error registrando audit log: {e}")

    @classmethod
    def log_logout(cls, user, request=None, metadata: Optional[dict] = None):
        logout_metadata = {
            'event': 'session_closed',
            'refresh_token_provided': bool(metadata.get('refresh_token_provided')) if metadata else False,
        }
        if metadata:
            logout_metadata.update(metadata)

        return cls.log(
            action=AuditLog.Action.LOGOUT,
            user=user,
            request=request,
            metadata=logout_metadata,
        )

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
    def log_data_access(cls, user, data_type: str, request=None, metadata: Optional[dict] = None):
        action_map = {
            'grades': AuditLog.Action.DATA_ACCESS_GRADES,
            'grades_history': AuditLog.Action.DATA_ACCESS_GRADES,
            'schedule': AuditLog.Action.DATA_ACCESS_SCHEDULE,
            'profile': AuditLog.Action.DATA_ACCESS_PROFILE,
            'stats': AuditLog.Action.DATA_ACCESS_STATS,
            'activities': AuditLog.Action.DATA_ACCESS_ACTIVITIES,
            'notifications': AuditLog.Action.DATA_ACCESS_NOTIFICATIONS,
            'submit_activity': AuditLog.Action.DATA_SUBMIT_ACTIVITY,
            'teacher_create_activity': AuditLog.Action.TEACHER_CREATE_ACTIVITY,
        }
        action = action_map.get(data_type, AuditLog.Action.DATA_ACCESS_PROFILE)
        event_metadata = {'data_type': data_type}
        if metadata:
            event_metadata.update(metadata)
        return cls.log(action=action, user=user, request=request, metadata=event_metadata)
