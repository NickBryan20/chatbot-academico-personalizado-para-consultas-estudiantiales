"""URLs raíz del proyecto."""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # API v1
    path('api/auth/', include('apps.authentication.urls')),
    path('api/students/', include('apps.students.urls')),
    path('api/chat/', include('apps.chatbot.urls')),
    path('api/rag/', include('apps.rag.urls')),
    path('api/voice/', include('apps.voice.urls')),
    path('api/logs/', include('apps.audit_logs.urls')),

    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
