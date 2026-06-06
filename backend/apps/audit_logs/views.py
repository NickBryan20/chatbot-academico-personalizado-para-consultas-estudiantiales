"""Views de audit logs — solo para administradores."""
from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination
from .models import AuditLog
from .serializers import AuditLogSerializer


class AuditLogPagination(PageNumberPagination):
    page_size = 50


class AuditLogListView(generics.ListAPIView):
    """Lista los logs de auditoría. Solo para staff/admins."""
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = AuditLogPagination

    def get_queryset(self):
        qs = AuditLog.objects.select_related('user').all()
        action = self.request.query_params.get('action')
        severity = self.request.query_params.get('severity')
        user_id = self.request.query_params.get('user_id')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if action:
            qs = qs.filter(action=action)
        if severity:
            qs = qs.filter(severity=severity)
        if user_id:
            qs = qs.filter(user_id=user_id)
        if start_date:
            qs = qs.filter(timestamp__gte=start_date)
        if end_date:
            qs = qs.filter(timestamp__lte=end_date)
        return qs

from rest_framework.views import APIView
from rest_framework.response import Response

class ChatbotUsageStatsView(APIView):
    """Estadísticas de uso del chatbot para auditoría."""
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        user_id = request.query_params.get('user_id')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        qs = AuditLog.objects.filter(action=AuditLog.Action.CHAT_QUERY)
        if user_id:
            qs = qs.filter(user_id=user_id)
        if start_date:
            qs = qs.filter(timestamp__gte=start_date)
        if end_date:
            qs = qs.filter(timestamp__lte=end_date)

        total_queries = qs.count()
        
        # También calcular tokens si se usó la metadata (opcional, pero útil)
        return Response({
            'total_queries': total_queries,
            'filters': {
                'user_id': user_id,
                'start_date': start_date,
                'end_date': end_date
            }
        })
