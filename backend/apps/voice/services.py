"""
Servicio de voz: Speech-to-Text (Whisper) y Text-to-Speech (OpenAI TTS).
"""
import logging
import base64
import re
from io import BytesIO

from django.conf import settings

logger = logging.getLogger(__name__)


class VoiceService:
    """Maneja transcripción de voz y síntesis de audio."""

    def get_client(self):
        from openai import OpenAI
        return OpenAI(api_key=settings.OPENAI_API_KEY)

    def speech_to_text(self, audio_file) -> str:
        """
        Transcribe audio a texto usando OpenAI Whisper.
        """
        client = self.get_client()
        try:
            # Asegurar que leemos el contenido y lo envolvemos correctamente
            file_content = audio_file.read()
            file_size = len(file_content)
            
            if file_size < 100: # Demasiado pequeño para ser un audio válido
                logger.warning(f"Audio recibido demasiado pequeño: {file_size} bytes")
                return ""

            # Creamos un objeto de archivo en memoria con nombre explícito
            buffer = BytesIO(file_content)
            buffer.name = "recording.webm" 

            transcription = client.audio.transcriptions.create(
                model=settings.OPENAI_WHISPER_MODEL,
                file=buffer,
                language='es',
                response_format='text',
            )
            logger.info(f"STT: '{transcription[:50]}...' ({file_size} bytes)")
            return transcription.strip()
        except Exception as e:
            logger.error(f"Error en STT: {e}")
            raise

    def _prepare_tts_text(self, text: str) -> str:
        """Limpia marcas visuales y adapta siglas para pronunciación en español."""
        cleaned = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
        cleaned = re.sub(r'`([^`]*)`', r'\1', cleaned)
        cleaned = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', cleaned)
        cleaned = re.sub(r'https?://\S+', ' enlace oficial ', cleaned)

        replacements = {
            'PUCE-SI': 'PUCE Sede Ibarra',
            'PUCESI': 'PUCE Sede Ibarra',
            'FAQ': 'preguntas frecuentes',
            'PDF': 'documento PDF',
            'NRC': 'ene erre ce',
            'URL': 'enlace',
            'OTP': 'código de verificación',
            '2FA': 'doble factor de autenticación',
            'IA': 'inteligencia artificial',
            'email': 'correo electrónico',
            'e-mail': 'correo electrónico',
            'online': 'en línea',
        }
        for source, target in replacements.items():
            cleaned = re.sub(rf'\b{re.escape(source)}\b', target, cleaned, flags=re.IGNORECASE)

        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        return cleaned[:700]

    def text_to_speech(self, text: str) -> bytes:
        """
        Convierte texto a audio MP3 usando OpenAI TTS.

        Args:
            text: Texto a convertir

        Returns:
            Bytes del archivo MP3
        """
        client = self.get_client()
        try:
            # Limitar texto para TTS (máximo ~500 chars para respuesta ágil)
            text_trimmed = self._prepare_tts_text(text)

            speech_kwargs = {
                'model': settings.OPENAI_TTS_MODEL,
                'voice': settings.OPENAI_TTS_VOICE,
                'input': text_trimmed,
                'response_format': 'mp3',
            }
            if str(settings.OPENAI_TTS_MODEL).startswith('gpt-4o-mini-tts'):
                speech_kwargs['instructions'] = settings.OPENAI_TTS_INSTRUCTIONS

            response = client.audio.speech.create(**speech_kwargs)

            audio_bytes = response.read()
            logger.info(f"TTS: {len(audio_bytes)} bytes generados")
            return audio_bytes
        except Exception as e:
            logger.error(f"Error en TTS: {e}")
            raise


voice_service = VoiceService()
