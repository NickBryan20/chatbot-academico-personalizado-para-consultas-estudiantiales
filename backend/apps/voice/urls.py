"""URLs del módulo de voz."""
from django.urls import path
from .views import SpeechToTextView, VoiceChatView

urlpatterns = [
    path('stt/', SpeechToTextView.as_view(), name='voice-stt'),
    path('chat/', VoiceChatView.as_view(), name='voice-chat'),
]
