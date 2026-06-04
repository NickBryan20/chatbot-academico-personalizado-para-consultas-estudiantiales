"""URLs del chatbot."""
from django.urls import path
from .views import ChatView, ConversationHistoryView, SessionListView

urlpatterns = [
    path('', ChatView.as_view(), name='chat'),
    path('history/', ConversationHistoryView.as_view(), name='chat-history'),
    path('sessions/', SessionListView.as_view(), name='chat-sessions'),
]
