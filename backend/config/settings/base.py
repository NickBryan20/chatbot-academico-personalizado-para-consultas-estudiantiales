"""
Django settings base para chatbot académico PUCESI.
Lee TODAS las variables sensibles desde variables de entorno (.env).
"""
import os
from pathlib import Path
from datetime import timedelta
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent.parent


def resolve_base_path(value: str) -> str:
    """Convierte rutas relativas del .env en rutas estables dentro de backend/."""
    path = Path(value)
    return str(path if path.is_absolute() else BASE_DIR / path)

# ── SEGURIDAD ─────────────────────────────────────────────────────────────────
SECRET_KEY = config('DJANGO_SECRET_KEY')
DEBUG = config('DJANGO_DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('DJANGO_ALLOWED_HOSTS', default='localhost').split(',')

AUTH_USER_MODEL = 'authentication.User'

# ── APLICACIONES ──────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'django_otp',
    'django_otp.plugins.otp_totp',
    'drf_spectacular',

    # Apps del proyecto
    'apps.authentication',
    'apps.students',
    'apps.chatbot',
    'apps.rag',
    'apps.voice',
    'apps.audit_logs',
]

# ── MIDDLEWARE ────────────────────────────────────────────────────────────────
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# ── BASE DE DATOS ─────────────────────────────────────────────────────────────
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
        'OPTIONS': {
            'connect_timeout': 10,
        },
    }
}

# ── VALIDACIÓN DE CONTRASEÑAS ─────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
     'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Usar Argon2 para hashing de contraseñas (más seguro que bcrypt)
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
]

# ── INTERNACIONALIZACIÓN ──────────────────────────────────────────────────────
LANGUAGE_CODE = 'es-ec'
TIME_ZONE = 'America/Guayaquil'
USE_I18N = True
USE_TZ = True

# ── ARCHIVOS ESTÁTICOS Y MEDIA ────────────────────────────────────────────────
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ── REST FRAMEWORK ────────────────────────────────────────────────────────────
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '20/minute',
        'user': '100/minute',
        'login': '5/minute',
    },
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
}

# ── JWT ───────────────────────────────────────────────────────────────────────
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(
        minutes=config('JWT_ACCESS_TOKEN_LIFETIME_MINUTES', default=15, cast=int)
    ),
    'REFRESH_TOKEN_LIFETIME': timedelta(
        days=config('JWT_REFRESH_TOKEN_LIFETIME_DAYS', default=7, cast=int)
    ),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
}

# ── CORS ──────────────────────────────────────────────────────────────────────
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='http://localhost:5173'
).split(',')
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'accept', 'accept-encoding', 'authorization',
    'content-type', 'dnt', 'origin', 'user-agent',
    'x-csrftoken', 'x-requested-with',
]

# ── EMAIL ─────────────────────────────────────────────────────────────────────
EMAIL_BACKEND = config(
    'EMAIL_BACKEND',
    default='django.core.mail.backends.console.EmailBackend'
)
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = 'PUCESI Chatbot <noreply@pucesi.edu.ec>'

# ── OTP ───────────────────────────────────────────────────────────────────────
OTP_EXPIRY_SECONDS = config('OTP_EXPIRY_SECONDS', default=300, cast=int)
OTP_LENGTH = config('OTP_LENGTH', default=6, cast=int)
SEED_STUDENT_PASSWORD = config('SEED_STUDENT_PASSWORD', default='')
SEED_TEACHER_PASSWORD = config('SEED_TEACHER_PASSWORD', default='')
SEED_ADMIN_PASSWORD = config('SEED_ADMIN_PASSWORD', default='')

# ── OPENAI ────────────────────────────────────────────────────────────────────
OPENAI_API_KEY = config('OPENAI_API_KEY', default='')
OPENAI_MODEL = config('OPENAI_MODEL', default='gpt-4o-mini')
OPENAI_EMBEDDING_MODEL = config('OPENAI_EMBEDDING_MODEL', default='text-embedding-3-small')
OPENAI_TTS_MODEL = config('OPENAI_TTS_MODEL', default='gpt-4o-mini-tts')
OPENAI_TTS_VOICE = config('OPENAI_TTS_VOICE', default='nova')
OPENAI_TTS_INSTRUCTIONS = config(
    'OPENAI_TTS_INSTRUCTIONS',
    default=(
        'Pronuncia todo el contenido en español latinoamericano neutral, '
        'con tono académico y natural. No cambies de idioma salvo nombres propios o materias.'
    )
)
OPENAI_WHISPER_MODEL = config('OPENAI_WHISPER_MODEL', default='whisper-1')

# ── RAG ───────────────────────────────────────────────────────────────────────
FAISS_INDEX_PATH = resolve_base_path(
    config('FAISS_INDEX_PATH', default=str(BASE_DIR / 'rag_index' / 'faiss_index'))
)
DOCUMENTS_PATH = resolve_base_path(
    config('DOCUMENTS_PATH', default=str(BASE_DIR / 'documents'))
)
RAG_TOP_K = config('RAG_TOP_K', default=5, cast=int)
RAG_CHUNK_SIZE = config('RAG_CHUNK_SIZE', default=500, cast=int)
RAG_CHUNK_OVERLAP = config('RAG_CHUNK_OVERLAP', default=50, cast=int)
RAG_EXCLUDED_SOURCE_FILES = [
    name.strip()
    for name in config('RAG_EXCLUDED_SOURCE_FILES', default='Estudiantes_Prueba.txt').split(',')
    if name.strip()
]

# ── FRONTEND ──────────────────────────────────────────────────────────────────
FRONTEND_URL = config('FRONTEND_URL', default='http://localhost:5173')

# ── SPECTACULAR (API Docs) ────────────────────────────────────────────────────
SPECTACULAR_SETTINGS = {
    'TITLE': 'Chatbot Académico PUCESI API',
    'DESCRIPTION': 'API REST para el sistema de chatbot académico inteligente de la PUCESI.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

# ── SEGURIDAD DE SESIONES Y COOKIES ──────────────────────────────────────────
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_HTTPONLY = False  # El frontend necesita leerla para enviarla
CSRF_COOKIE_SAMESITE = 'Lax'
