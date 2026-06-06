"""Views del módulo de voz: STT, TTS y procesamiento completo voz-a-voz."""
import base64
import uuid
import logging

from django.conf import settings
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..students.models import Student
from ..chatbot.services import chatbot_service
from .services import voice_service

logger = logging.getLogger(__name__)


class SpeechToTextView(APIView):
    """Transcribe audio a texto usando Whisper."""
    permission_classes = [IsAuthenticated]
    throttle_scope = 'voice'

    def post(self, request):
        audio_file = request.FILES.get('audio')
        if not audio_file:
            return Response(
                {'error': 'No se recibió archivo de audio.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if audio_file.size > settings.MAX_AUDIO_UPLOAD_BYTES:
            return Response(
                {'error': 'El archivo de audio supera el tamaño máximo permitido.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            transcript = voice_service.speech_to_text(audio_file)
            return Response({'transcript': transcript})
        except Exception as e:
            logger.error(f"Error STT: {e}")
            return Response(
                {'error': 'Error al transcribir el audio.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class VoiceChatView(APIView):
    """
    Procesamiento completo de voz a voz:
    Soporta acceso público (solo RAG) y privado (RAG + Datos Estudiante).
    """
    permission_classes = [AllowAny]
    throttle_scope = 'voice'

    def post(self, request):
        audio_file = request.FILES.get('audio')
        session_id = request.data.get('session_id') or str(uuid.uuid4())

        if not audio_file:
            return Response(
                {'error': 'No se recibió archivo de audio.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if audio_file.size > settings.MAX_AUDIO_UPLOAD_BYTES:
            return Response(
                {'error': 'El archivo de audio supera el tamaño máximo permitido.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Identificar estudiante solo si el usuario está autenticado
        student = None
        if request.user and request.user.is_authenticated:
            try:
                student = Student.objects.get(user=request.user)
            except Student.DoesNotExist:
                pass # Autenticado pero sin perfil (ej: admin)

        try:
            # 1. STT: audio → texto
            transcript = voice_service.speech_to_text(audio_file)

            if not transcript:
                return Response(
                    {'error': 'No se pudo transcribir el audio. Intenta hablar más claro.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if len(transcript) > settings.CHAT_MAX_MESSAGE_LENGTH:
                return Response(
                    {'error': 'La transcripción supera la longitud máxima permitida.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 2. Chatbot: texto → respuesta
            chat_result = chatbot_service.generate_response(
                student=student,
                user_message=transcript,
                session_id=session_id,
                request=request,
            )

            response_text = chat_result['response']

            # 3. TTS: respuesta → audio
            audio_b64 = None
            audio_error = None
            try:
                audio_bytes = voice_service.text_to_speech(response_text)
                audio_b64 = base64.b64encode(audio_bytes).decode('utf-8')
            except Exception as tts_error:
                audio_error = 'No se pudo generar audio para esta respuesta.'
                logger.error(f"Error TTS en voice chat: {tts_error}")

            return Response({
                'transcript': transcript,
                'response': response_text,
                'audio_base64': audio_b64,
                'audio_format': 'mp3' if audio_b64 else None,
                'audio_error': audio_error,
                'session_id': session_id,
                'tokens_used': chat_result.get('tokens_used', 0),
            })

        except Exception as e:
            logger.error(f"Error en voice chat: {e}")
            return Response(
                {'error': 'Error procesando el mensaje de voz.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
