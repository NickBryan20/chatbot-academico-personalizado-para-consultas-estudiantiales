import uuid
import logging
import base64

from django.conf import settings
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..students.models import Student, ConversationHistory
from ..voice.services import voice_service
from .services import chatbot_service

logger = logging.getLogger(__name__)

class ChatView(APIView):
    """
    Endpoint principal del chatbot.
    Soporta acceso público (solo RAG institucional) y privado (RAG + Datos Estudiante).
    Ahora incluye soporte de voz (TTS) para todas las respuestas.
    """
    permission_classes = [AllowAny]
    throttle_scope = 'chat'

    def post(self, request):
        raw_message = request.data.get('message', '')
        message = str(raw_message).strip() if raw_message is not None else ''
        session_id = request.data.get('session_id') or str(uuid.uuid4())

        if not message:
            return Response(
                {'error': 'El mensaje no puede estar vacío.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if len(message) > settings.CHAT_MAX_MESSAGE_LENGTH:
            return Response(
                {'error': 'El mensaje supera la longitud máxima permitida.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Identificar estudiante solo si el usuario está autenticado
        student = None
        if request.user and request.user.is_authenticated:
            try:
                student = Student.objects.get(user=request.user)
            except Student.DoesNotExist:
                pass 

        # Generar respuesta
        result = chatbot_service.generate_response(
            student=student,
            user_message=message,
            session_id=session_id,
            request=request,
        )

        response_text = result.get('response', '')
        
        # Generar Audio (TTS) para que siempre hable
        try:
            audio_bytes = voice_service.text_to_speech(response_text)
            audio_b64 = base64.b64encode(audio_bytes).decode('utf-8')
            result['audio_base64'] = audio_b64
            result['audio_format'] = 'mp3'
        except Exception as e:
            logger.error(f"Error generando TTS en ChatView: {e}")
            result['audio_error'] = 'No se pudo generar audio para esta respuesta.'
            result['audio_format'] = None

        return Response(result, status=status.HTTP_200_OK)


class ConversationHistoryView(APIView):
    """Retorna el historial de conversaciones del estudiante."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            return Response({'error': 'Perfil no encontrado.'}, status=404)

        session_id = request.query_params.get('session_id')

        qs = ConversationHistory.objects.filter(student=student)
        if session_id:
            qs = qs.filter(session_id=session_id)

        # Últimas 50 entradas
        qs = qs.order_by('-timestamp')[:50]

        data = [{
            'id': str(msg.id),
            'role': msg.role,
            'message': msg.message,
            'timestamp': msg.timestamp.isoformat(),
            'session_id': str(msg.session_id),
            'tokens_used': msg.tokens_used,
        } for msg in reversed(list(qs))]

        return Response({'messages': data})


class SessionListView(APIView):
    """Lista todas las sesiones de conversación del estudiante."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            return Response({'error': 'Perfil no encontrado.'}, status=404)

        # Obtener sesiones únicas
        sessions = (
            ConversationHistory.objects
            .filter(student=student)
            .values('session_id')
            .annotate(
                last_message=__import__('django.db.models', fromlist=['Max']).Max('timestamp'),
                message_count=__import__('django.db.models', fromlist=['Count']).Count('id'),
            )
            .order_by('-last_message')[:20]
        )

        return Response({'sessions': list(sessions)})
