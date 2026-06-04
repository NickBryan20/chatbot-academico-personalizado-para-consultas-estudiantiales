"""Serializers del módulo de audit logs."""
from rest_framework import serializers
from .models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = AuditLog
        fields = ['id', 'username', 'action', 'severity', 'ip_address',
                  'metadata', 'timestamp']

    def get_username(self, obj):
        return obj.user.username if obj.user else 'Anónimo'
