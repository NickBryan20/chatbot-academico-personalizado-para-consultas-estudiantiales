"""URL del módulo RAG: construcción del índice (solo admins)."""
from django.urls import path
from .views import BuildIndexView, RAGSearchView

urlpatterns = [
    path('build/', BuildIndexView.as_view(), name='rag-build'),
    path('search/', RAGSearchView.as_view(), name='rag-search'),
]
