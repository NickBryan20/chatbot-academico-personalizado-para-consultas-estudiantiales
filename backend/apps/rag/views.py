"""Views del módulo RAG."""
import logging

from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .engine import rag_engine
from apps.audit_logs.models import AuditLog
from apps.audit_logs.services import AuditLogService

logger = logging.getLogger(__name__)


class BuildIndexView(APIView):
    """Construye o reconstruye el índice FAISS. Solo admins."""
    permission_classes = [IsAdminUser]

    def post(self, request):
        force = request.data.get('force', False)
        try:
            rag_engine.build_index(force_rebuild=force)
            AuditLogService.log(
                action=AuditLog.Action.RAG_INDEX_BUILD,
                user=request.user,
                request=request,
                metadata={'force': force}
            )
            return Response({'message': 'Índice RAG construido correctamente.'})
        except Exception as e:
            logger.error(f"Error construyendo índice RAG: {e}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RAGSearchView(APIView):
    """Busca en el índice RAG. Para pruebas y depuración."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        query = request.data.get('query', '').strip()
        if not query:
            return Response({'error': 'Query requerida.'}, status=400)

        results = rag_engine.search(query)
        return Response({'results': results, 'count': len(results)})
