"""Serializers del módulo de audit logs."""
from rest_framework import serializers
from .models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    user_full_name = serializers.SerializerMethodField()
    user_role = serializers.SerializerMethodField()
    action_display = serializers.CharField(source='get_action_display', read_only=True)
    severity_display = serializers.CharField(source='get_severity_display', read_only=True)

    class Meta:
        model = AuditLog
        fields = [
            'id', 'user_id', 'username', 'user_full_name', 'user_role',
            'action', 'action_display', 'severity', 'severity_display',
            'ip_address', 'user_agent', 'metadata', 'timestamp',
        ]

    def get_username(self, obj):
        return obj.user.username if obj.user else 'Anónimo'

    def get_user_id(self, obj):
        return str(obj.user_id) if obj.user_id else None

    def get_user_full_name(self, obj):
        if not obj.user:
            return 'Anónimo'
        return obj.user.get_full_name() or obj.user.username

    def get_user_role(self, obj):
        if not obj.user:
            return 'anonymous'
        return getattr(obj.user, 'effective_role', getattr(obj.user, 'role', ''))
