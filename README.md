# 🎓 Chatbot Académico IA - PUCE-SI (Prototipo Tesis)

![Arquitectura del Sistema](https://img.shields.io/badge/Architecture-RAG_|_Django_|_React-blue) ![Estado](https://img.shields.io/badge/Status-Prototipo_Avanzado-success) ![Seguridad](https://img.shields.io/badge/Security-ISO_27001_|_JWT_|_Argon2-critical)

Este repositorio contiene el código fuente completo del prototipo del **Chatbot Académico Inteligente** desarrollado para la Pontificia Universidad Católica del Ecuador Sede Ibarra (PUCE-SI). El sistema está diseñado bajo estrictos estándares de seguridad y cuenta con una arquitectura de Generación Aumentada por Recuperación (RAG) para ofrecer información institucional veraz, junto con integración nativa al expediente del estudiante.

## 📊 Resumen general del proyecto

- 2 bloques principales: `frontend/` y `backend/`
- 6 aplicaciones Django en el backend
- 5 páginas React en el frontend
- 10 tablas principales en la base de datos
- 13 acciones auditables definidas en el sistema
- 3 documentos institucionales de conocimiento usados por RAG

Consulta `backend/README.md` y `frontend/README.md` para obtener la documentación detallada de cada bloque.

---

## 🏛️ Arquitectura del Sistema

El proyecto está dividido en dos grandes bloques que se comunican a través de una API RESTful segura:

1. **Frontend (Cliente):** SPA desarrollada en React y TypeScript, usando Vite y TailwindCSS. Diseñada con un enfoque "Dark Mode" premium y Glassmorphism para los estudiantes.
2. **Backend (Servidor):** API desarrollada en Python con Django REST Framework. Actúa como el cerebro central, orquestando la base de datos, el RAG, las llamadas a OpenAI y los registros de auditoría.

### 🧠 Flujo de la Inteligencia Artificial (RAG)

El Chatbot no es un LLM genérico. Su comportamiento se rige por la arquitectura **RAG (Retrieval-Augmented Generation)**:
- **Base de Conocimiento:** Todos los documentos institucionales, precios, tours virtuales y mallas académicas residen en `/backend/documents/`.
- **Scraping Automático:** Se ejecuta un *scraper* web en el backend (`scrape_rag_links.py`) que absorbe contenido de la web oficial de PUCE-SI y lo inyecta a los documentos base.
- **Motor Vectorial (FAISS):** Los documentos se dividen en *chunks* y se convierten en vectores semánticos (Embeddings de OpenAI). Al hacer una pregunta, el sistema busca los vectores más relevantes antes de generar una respuesta.
- **Contexto Personalizado:** Si el usuario ha iniciado sesión, el backend *inyecta* silenciosamente su historial de notas, asistencias, deberes pendientes y horarios en el *prompt* maestro del LLM. Así, el bot sabe exactamente con quién está hablando.

---

## 🔐 Seguridad del Sistema (Sprint 5 — Detalle Completo)

El sistema implementa un modelo de seguridad en capas (*Defense in Depth*) alineado con los controles de la norma **ISO 27001** para garantizar la confidencialidad, integridad y disponibilidad de los datos académicos. A continuación se detalla cada capa implementada en el código fuente.

### 1. 🔑 Hashing de Contraseñas — Argon2

Las contraseñas **nunca** se almacenan en texto plano. El sistema utiliza **Argon2** como algoritmo principal de hashing, considerado el más robusto de la industria actual (ganador del Password Hashing Competition 2015). Argon2 es resistente a ataques de fuerza bruta con GPU/ASIC gracias a su diseño *memory-hard*.

**Configuración en el código** (`backend/config/settings/base.py`, línea 104):
```python
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',  # Principal
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',  # Fallback
]
```

Adicionalmente, se aplican **4 validadores de contraseña** para garantizar complejidad mínima:
- `UserAttributeSimilarityValidator` — Prohíbe contraseñas similares al nombre de usuario.
- `MinimumLengthValidator` — Longitud mínima de 8 caracteres.
- `CommonPasswordValidator` — Rechaza las 20,000 contraseñas más comunes.
- `NumericPasswordValidator` — Prohíbe contraseñas exclusivamente numéricas.

### 2. 🎫 Autenticación con JWT (JSON Web Tokens)

El sistema utiliza **Simple JWT** para gestionar sesiones sin estado (*stateless*). Cada sesión autenticada se gestiona mediante un par de tokens:

| Token | Vida Útil | Propósito |
|:---|:---|:---|
| **Access Token** | 15 minutos | Autenticar cada petición HTTP (cabecera `Authorization: Bearer <token>`) |
| **Refresh Token** | 7 días | Obtener un nuevo Access Token sin re-autenticar al usuario |

**Configuración en el código** (`backend/config/settings/base.py`, línea 147):
```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,          # Cada refresh genera un nuevo par
    'BLACKLIST_AFTER_ROTATION': True,        # El refresh anterior se invalida
    'UPDATE_LAST_LOGIN': True,               # Actualiza last_login del usuario
    'ALGORITHM': 'HS256',                    # Algoritmo de firma
    'AUTH_HEADER_TYPES': ('Bearer',),
}
```

**Ciclo de vida del token:**
1. El usuario se autentica → recibe `access` + `refresh`.
2. El `access` expira en 15 min → el frontend envía el `refresh` a `/api/token/refresh/`.
3. Se emite un **nuevo par** de tokens y el `refresh` anterior se añade a la **blacklist** (tabla `token_blacklist_outstandingtoken`).
4. Al cerrar sesión (`POST /api/auth/logout/`), el refresh token se invalida explícitamente.

### 3. 📱 Autenticación de Dos Factores (2FA / OTP)

El sistema implementa autenticación de doble factor basada en **códigos OTP temporales** enviados por correo electrónico institucional (`@pucesi.edu.ec`).

**Flujo completo:**
1. El estudiante ingresa su código de usuario y contraseña.
2. Si las credenciales son válidas y el usuario tiene `is_2fa_enabled=True`, el backend genera un OTP de **6 dígitos** numéricos aleatorios.
3. El OTP se almacena en la tabla `auth_otp_token` con un campo `expires_at` (5 minutos de validez) y un `temp_token` UUID para la verificación.
4. Se invalidan **todos los OTP anteriores no usados** del usuario (prevención de reutilización).
5. El código se envía al email del estudiante.
6. El estudiante ingresa el código en el formulario de verificación.
7. El backend valida: (a) que el OTP no haya expirado, (b) que no haya sido usado previamente, (c) que coincida el `temp_token`.
8. Si es válido, se emiten los tokens JWT y se marca el OTP como `is_used=True`.

**Implementación en el código:**
- Modelo OTP: `backend/apps/authentication/models.py` — clase `OTPToken` (línea 62)
- Servicio OTP: `backend/apps/authentication/services.py` — clase `OTPService` (línea 18)
- Controlador: `backend/apps/authentication/controllers.py` — `AuthenticationController` (línea 18)

### 4. 🚫 Bloqueo de Cuentas por Intentos Fallidos

Para mitigar ataques de fuerza bruta, el sistema implementa un **mecanismo automático de bloqueo de cuentas**:

- Tras **5 intentos fallidos consecutivos**, la cuenta se bloquea automáticamente durante **15 minutos**.
- El bloqueo se almacena en el campo `account_locked_until` del modelo `User`.
- Tras un login exitoso, el contador se reinicia a 0.

**Implementación en el código** (`backend/apps/authentication/models.py`, línea 48):
```python
def increment_failed_attempts(self):
    self.failed_login_attempts += 1
    if self.failed_login_attempts >= 5:
        self.account_locked_until = timezone.now() + timezone.timedelta(minutes=15)
    self.save(update_fields=['failed_login_attempts', 'account_locked_until'])

def reset_failed_attempts(self):
    self.failed_login_attempts = 0
    self.account_locked_until = None
    self.save(update_fields=['failed_login_attempts', 'account_locked_until'])
```

### 5. ⏱️ Rate Limiting (Throttling)

Para prevenir ataques de denegación de servicio (DoS) y abuso de la API, se aplica **limitación de tasa** en tres niveles:

| Nivel | Límite | Protege |
|:---|:---|:---|
| **Anónimo** (`anon`) | 20 req/min | Endpoints públicos (RAG, información general) |
| **Autenticado** (`user`) | 100 req/min | Endpoints del dashboard, chatbot, perfil |
| **Login** (`login`) | 5 req/min | Endpoint de autenticación (evita fuerza bruta) |

**Configuración en el código** (`backend/config/settings/base.py`, línea 132):
```python
'DEFAULT_THROTTLE_RATES': {
    'anon': '20/minute',
    'user': '100/minute',
    'login': '5/minute',
}
```

### 6. 🌐 CORS y Cabeceras de Seguridad

La comunicación entre el frontend (React, puerto 5173) y el backend (Django, puerto 8000) está restringida por **CORS (Cross-Origin Resource Sharing)**:

- Solo los orígenes declarados en `CORS_ALLOWED_ORIGINS` pueden realizar peticiones.
- Se permiten credenciales (`CORS_ALLOW_CREDENTIALS = True`).
- Las cabeceras permitidas están explícitamente enumeradas (whitelist).

Adicionalmente, el sistema implementa las siguientes **cabeceras de seguridad**:

| Cabecera | Valor | Protección |
|:---|:---|:---|
| `SESSION_COOKIE_HTTPONLY` | `True` | Previene acceso a cookies de sesión desde JavaScript (XSS) |
| `SESSION_COOKIE_SAMESITE` | `Lax` | Previene envío de cookies en peticiones cross-site (CSRF) |
| `X-Frame-Options` | Middleware activado | Previene Clickjacking (inyección en iframe) |
| `SecurityMiddleware` | Activado | Aplica cabeceras de seguridad estándar de Django |

### 7. 🔒 UUIDs y Variables de Entorno

**UUIDs como llaves primarias:** Todas las tablas del sistema (User, Student, AuditLog, OTPToken, etc.) utilizan `UUIDv4` como llave primaria en lugar de IDs autoincrementales. Esto previene **ataques de enumeración** donde un atacante podría adivinar IDs secuenciales (ej: `/api/student/1`, `/api/student/2`).

**Variables de entorno (`.env`):** Todas las credenciales sensibles se leen desde variables de entorno usando `python-decouple`, **nunca** se escriben en el código fuente:
- `DJANGO_SECRET_KEY` — Clave secreta de Django
- `DB_NAME`, `DB_USER`, `DB_PASSWORD` — Credenciales de PostgreSQL
- `OPENAI_API_KEY` — Clave de la API de OpenAI
- `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` — Credenciales SMTP

---

## 📋 Auditoría del Sistema (ISO 27001 — Detalle Completo)

El sistema implementa un **registro de auditoría centralizado** que cumple con los principios de trazabilidad, no repudio e inmutabilidad exigidos por la norma ISO 27001. Cada acción crítica del sistema queda estampada en la tabla `audit_log` con fines forenses y estadísticos.

### Modelo de Datos de Auditoría

La tabla `audit_log` almacena los siguientes campos:

| Campo | Tipo | Descripción |
|:---|:---|:---|
| `id` | UUID (PK) | Identificador único no enumerable |
| `user_id` | UUID (FK) | Usuario que realizó la acción (null si anónimo) |
| `action` | VARCHAR(50) | Código de acción (ver tabla de acciones) |
| `severity` | VARCHAR(10) | Nivel: `INFO`, `WARNING`, `CRITICAL` |
| `ip_address` | IP | Dirección IP real del cliente (soporta X-Forwarded-For para proxies) |
| `user_agent` | TEXT | Navegador/dispositivo del usuario |
| `metadata` | JSON | Datos contextuales del evento (query preview, tokens usados, razón de fallo, etc.) |
| `timestamp` | DATETIME | Marca de tiempo automática (indexada para consultas rápidas) |

### Acciones Auditadas

El sistema audita las siguientes **13 acciones** organizadas por categoría:

| Categoría | Código de Acción | Descripción | Severidad |
|:---|:---|:---|:---|
| **Autenticación** | `LOGIN_SUCCESS` | Inicio de sesión exitoso | INFO |
| | `LOGIN_FAILED` | Intento de login fallido | WARNING |
| | `LOGIN_OTP_SENT` | Código OTP enviado al email | INFO |
| | `LOGOUT` | Cierre de sesión | INFO |
| | `ACCOUNT_LOCKED` | Cuenta bloqueada por intentos fallidos | CRITICAL |
| **Chatbot** | `CHAT_QUERY` | Consulta de texto al chatbot | INFO |
| | `CHAT_VOICE_QUERY` | Consulta de voz al chatbot | INFO |
| **Datos Académicos** | `DATA_ACCESS_GRADES` | Estudiante consultó sus calificaciones | INFO |
| | `DATA_ACCESS_SCHEDULE` | Estudiante consultó sus horarios | INFO |
| | `DATA_ACCESS_PROFILE` | Estudiante consultó su perfil académico | INFO |
| **RAG** | `RAG_QUERY` | Búsqueda en el índice vectorial | INFO |
| | `RAG_INDEX_BUILD` | Reconstrucción del índice FAISS | INFO |
| **Sistema** | `SYSTEM_ERROR` | Error interno del sistema | CRITICAL |

### Servicio Centralizado de Auditoría

Todos los módulos del sistema registran eventos a través de un **servicio único** (`AuditLogService`) que garantiza consistencia y previene que errores de logging interrumpan el flujo principal:

**Implementación** (`backend/apps/audit_logs/services.py`):
- `AuditLogService.log()` — Método estático principal. Extrae automáticamente la IP (soporta `X-Forwarded-For`) y el User-Agent del request HTTP.
- `AuditLogService.log_login_failed()` — Registra intentos fallidos con severidad `WARNING` e incluye el número de intentos en la metadata.
- `AuditLogService.log_chat_query()` — Registra consultas al chatbot con preview de la pregunta y respuesta (primeros 100 caracteres) y tokens consumidos.
- `AuditLogService.log_data_access()` — Registra accesos a datos académicos (notas, horarios, perfil).

### Índices de Base de Datos para Auditoría

Para garantizar consultas rápidas sobre la tabla de auditoría (que puede crecer significativamente), se implementaron **3 índices compuestos**:

```python
indexes = [
    models.Index(fields=['user', 'timestamp']),      # Buscar por usuario + fecha
    models.Index(fields=['action', 'timestamp']),     # Buscar por tipo de acción + fecha
    models.Index(fields=['severity', 'timestamp']),   # Buscar por severidad + fecha
]
```

### Dashboard de Auditoría (Administrador)

El sistema expone dos endpoints exclusivos para administradores:

| Endpoint | Método | Descripción |
|:---|:---|:---|
| `GET /api/audit-logs/` | GET | Lista paginada de logs (50 por página) con filtros por `action` y `severity` |
| `GET /api/audit-logs/stats/` | GET | Estadísticas de uso del chatbot con filtros por `user_id`, `start_date`, `end_date` |

Ambos endpoints requieren permiso `IsAdminUser` (solo staff puede acceder).

---

## 🗄️ Modelo de Base de Datos

El sistema utiliza **PostgreSQL** con un modelado fuertemente tipado:
- **Autenticación (JWT):** Gestión de sesiones seguras y asíncronas con Tokens que se refrescan. Cifrado nativo de contraseñas mediante **Argon2** (mitiga ataques de fuerza bruta).
- **Estudiantes y Expedientes:** Relaciones complejas (One-to-Many, Many-to-Many) entre `Estudiante`, `Materia`, `Horario` y `Calificacion`.
- **Auditoría (ISO 27001):** Cada acción que realiza el estudiante (como usar el chatbot, consultar notas o subir un deber) queda estampada en la tabla `AuditLog` con su respectiva IP y estampa de tiempo para fines forenses y estadísticos.

---

## 🤔 Preguntas Frecuentes (Defensa de Tesis)

Para facilitar la revisión técnica del tribunal, aquí se responden las preguntas clave sobre el código:

**1. ¿Dónde se configura la conexión a la Base de Datos?**
Toda la conexión a PostgreSQL o SQLite está configurada centralmente en el archivo `backend/config/settings/base.py` (Línea 80, diccionario `DATABASES`). Usa variables de entorno (`.env`) por seguridad.

**2. ¿Dónde exactamente se aplica el motor RAG en el código?**
El motor RAG se invoca cada vez que un estudiante envía un mensaje. Esto ocurre en el archivo `backend/apps/chatbot/services.py` dentro de la función `generate_response()` (aproximadamente en la Línea 200). Allí verás cómo la función `rag_engine.search(user_message)` extrae los fragmentos relevantes y luego se inyectan en el *prompt* de OpenAI.

**3. ¿Cómo "sabe" el chatbot las notas del estudiante?**
En el mismo archivo `backend/apps/chatbot/services.py`, la función `get_student_context()` (Líneas 95-150) consulta las calificaciones y horarios del estudiante directamente de la base de datos y arma un texto invisible que se adjunta al contexto de la Inteligencia Artificial.

**4. ¿Dónde se encuentra el Web Scraper automatizado?**
El script que construimos para extraer datos de la web de la PUCE-SI está en `backend/scripts/scrape_rag_links.py`. Descarga el texto de los enlaces de `puce_ibarra_info.txt` y genera el `scraped_web_content.txt`.

**5. ¿Dónde está la lógica de la Auditoría?**
La auditoría global ocurre en `backend/apps/audit_logs/services.py` y se registra utilizando el interceptor `AuditLogService.log()`. En la API, el endpoint visual de auditoría se encuentra en `backend/apps/audit_logs/views.py` (clase `ChatbotUsageStatsView`).

**6. ¿Dónde está la personalización/prompt del chatbot?**
Las instrucciones base (el "alma" del chatbot) están en la constante `SYSTEM_PROMPT` dentro del archivo `backend/apps/chatbot/services.py` (Línea 11). Ahí se le ordena actuar como un asesor académico exclusivo de la PUCE-SI, con tono amable y profesional.

**7. ¿Por qué este chatbot es diferente a usar ChatGPT directamente?**
Un ChatGPT estándar sufre de "alucinaciones" (inventa respuestas si no sabe) y no tiene memoria institucional. Este proyecto soluciona eso mediante la arquitectura RAG: el modelo de IA está "obligado" a leer los documentos de la universidad (`documents/`) antes de responder. Además, este chatbot es "Context-Aware"; reconoce al estudiante que inició sesión, su carrera, sus notas y sus tareas pendientes, algo que un bot genérico jamás podría hacer.

**8. ¿Por qué elegir este desarrollo por encima de bots pre-fabricados?**
Los bots integrados genéricos suelen ser de tipo "Árbol de Decisión" (presione 1 para X, 2 para Y) y carecen de entendimiento semántico. Este desarrollo, al ser nativo, ofrece:
- **Trazabilidad Forense:** Control total sobre los datos, cumpliendo la norma ISO 27001 (Audit Logs).
- **Escalabilidad:** Al estar hecho en Django, se pueden añadir módulos enteros (pagos, matrículas) e inyectarlos al bot de forma natural sin depender de APIs de terceros.
- **Voz-a-Texto Nativo:** Integración directa con Whisper sin pasar por interfaces externas.

**9. ¿Cómo protege el sistema las contraseñas de los estudiantes?**
Las contraseñas se hashean con **Argon2** (el algoritmo ganador de la Password Hashing Competition), que es resistente a ataques con GPU/ASIC por su diseño memory-hard. Además, se aplican 4 validadores que rechazan contraseñas débiles, cortas, comunes o puramente numéricas. El hash resultante es irreversible: ni siquiera un administrador puede ver la contraseña original.

**10. ¿Qué pasa si alguien intenta fuerza bruta en el login?**
Tres capas de defensa actúan simultáneamente:
1. **Rate Limiting:** Solo se permiten 5 intentos de login por minuto por IP.
2. **Bloqueo de Cuenta:** Tras 5 intentos fallidos consecutivos, la cuenta se bloquea automáticamente durante 15 minutos.
3. **Auditoría:** Cada intento fallido queda registrado con severidad `WARNING`, incluyendo la IP del atacante y el número de intentos acumulados.

**11. ¿Cómo funciona la autenticación de dos factores?**
Tras validar usuario/contraseña, el sistema genera un código OTP de 6 dígitos aleatorios, lo almacena cifrado en la base de datos con una expiración de 5 minutos, y lo envía al correo institucional del estudiante. El código solo puede usarse una vez. Los OTP anteriores se invalidan automáticamente al generar uno nuevo. En desarrollo, el código se imprime en la consola del backend para pruebas.

**12. ¿Por qué se usan UUIDs en lugar de IDs numéricos?**
Los IDs autoincrementales (1, 2, 3...) son predecibles: un atacante puede enumerar todos los registros incrementando el ID. Los UUIDv4 son criptográficamente aleatorios (128 bits de entropía), haciendo prácticamente imposible adivinar el ID de otro usuario. Esto es una práctica recomendada por OWASP.

---

## 🚀 Despliegue Rápido

Para instrucciones detalladas sobre cómo ejecutar cada módulo, por favor consulta la documentación específica:
- 👉 [Documentación del Backend (Django)](./backend/README.md)
- 👉 [Documentación del Frontend (React)](./frontend/README.md)

---
*Desarrollado para la sustentación de Tesis. Todos los derechos reservados PUCE-SI 2026.*
