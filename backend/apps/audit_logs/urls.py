"""URLs del módulo de audit logs."""
from django.urls import path
from .views import AuditLogListView, ChatbotUsageStatsView

urlpatterns = [
    path('', AuditLogListView.as_view(), name='audit-logs-list'),
    path('chatbot-usage/', ChatbotUsageStatsView.as_view(), name='chatbot-usage-stats'),
]
