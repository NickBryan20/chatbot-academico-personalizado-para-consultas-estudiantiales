# ⚙️ Backend (Django REST Framework) - Chatbot PUCE-SI

Este directorio contiene el servidor principal del prototipo de tesis. Está desarrollado con Django REST Framework y sigue un patrón de capas claro: Modelos (ORM), Servicios/Controladores, Serializadores y Vistas API.

## 📊 Resumen estadístico del backend

- 6 aplicaciones (`apps/`): `authentication`, `students`, `audit_logs`, `chatbot`, `rag`, `voice`
- 10 modelos principales en la base de datos
- Más de 20 endpoints API expuestos entre autenticación, estudiantes, docentes, chatbot, RAG, voz y auditoría
- 13 acciones de auditoría definidas en `apps/audit_logs/models.py`
- 4 documentos institucionales de conocimiento en `backend/documents/`
- 1 índice FAISS en `backend/rag_index/faiss_index`

## 🗂️ Estructura de Módulos (Apps)

- `apps/authentication`: Manejo seguro de inicio de sesión, integración de 2FA (OTP) y rotación de tokens JWT.
- `apps/students`: Módulo académico central. Contiene las entidades `Estudiante`, `Materia`, `Horario`, `Matrícula`, `Calificación`, así como el flujo de entrega de `Actividad`.
- `apps/audit_logs`: Sistema de trazabilidad que registra eventos de seguridad, consultas de chatbot y accesos a datos académicos.
- `apps/chatbot`: Motor conversacional que integra RAG y personalización del contexto del estudiante antes de llamar a OpenAI.
- `apps/rag`: Controla la construcción y búsqueda en el índice vectorial FAISS.
- `apps/voice`: Gestión de conversión de voz a texto y respuestas de texto a voz.

## 🗄️ Base de datos

### Tablas y modelos principales

- `auth_user` (Usuario)
- `auth_otp_token` (OTP temporal)
- `student` (Perfil académico del estudiante)
- `professor` (Docente)
- `classroom` (Aulas/laboratorios)
- `subject` (Materia)
- `schedule` (Horario de clase)
- `enrollment` (Matrícula de estudiante)
- `grade` (Notas académicas)
- `audit_log` (Registro de auditoría)

### Relaciones principales

- `User` 1:1 `Student`
- `Student` 1:N `Enrollment`
- `Student` 1:N `Grade`
- `Schedule` N:1 `Subject`
- `Schedule` N:1 `Professor`
- `Professor` 1:1 `User` para acceso docente al aula virtual
- `Schedule` N:1 `Classroom`
- `Enrollment` N:1 `Schedule`
- `Grade` N:1 `Subject`
- `AuditLog` N:1 `User` (nullable)

### Detalle de atributos críticos

- `student.student_code`: Identificador académico único.
- `student.carrera`: Lista de 16 carreras normalizadas (`IDS`, `ITI`, `ADM`, `AGR`, `ZOO`, `VET`, `ENF`, `DER`, `ARQ`, `NEG`, `GAS`, `DIS`, `AUD`, `CIV`, `IAM`, `PED`).
- `grade` almacena hasta 5 valores de evaluación: `partial_1`, `partial_2`, `partial_3`, `final_exam`, `final_grade` y `attendance_percentage`.
- `enrollment` incluye `academic_period` y evita duplicados con la restricción única `student + schedule + academic_period`.
- `audit_log.metadata` es un campo JSON que guarda contexto adicional de cada evento.

## 🧠 RAG (Retrieval-Augmented Generation)

### Componentes de RAG

- Documentos fuente en `backend/documents/`:
  - `informacion_institucional.txt`
  - `puce_ibarra_info.txt`
  - `campus_mapa_servicios.txt`
  - `scraped_web_content.txt`
- `Estudiantes_Prueba.txt` se mantiene fuera del RAG y de GitHub porque contiene datos locales de prueba.
- Motor FAISS localizado en `backend/rag_index/faiss_index`
- Script de reconstrucción del índice: `backend/scripts/rebuild_rag_index.py`
- Scraper automático para extraer contenido web: `backend/scripts/scrape_rag_links.py`
- Lógica de búsqueda semántica: `apps/rag/engine.py`

### Flujo de trabajo RAG

1. Los documentos se leen desde `backend/documents/` y se vectorizan.
2. FAISS construye un índice semántico de los fragmentos de texto.
3. En cada consulta del chatbot, el backend ejecuta una búsqueda semántica en FAISS.
4. Los fragmentos se reordenan por prioridad: documentos validados del proyecto primero; scraping de la web oficial después.
5. El resultado final es una respuesta contextualizada, precisa y alineada a la información institucional.

### Métricas relevantes de RAG

- 4 archivos institucionales de conocimiento fuente.
- 1 índice vectorial persistente en disco.
- 1 script de reconstrucción para mantener el índice actualizado.
- 1 servicio que combina búsqueda semántica con contexto académico.

## 🔐 Seguridad

### Controles implementados

- `Argon2` para hashing de contraseñas.
- JWT con refresh token rotativo y blacklist.
- Autenticación de doble factor (2FA / OTP).
- Bloqueo automático de cuenta tras 5 intentos fallidos.
- Rate limiting en API: `anon`, `user`, `login`.
- CORS restringido a orígenes permitidos.
- Cookies `HTTPOnly` y `SameSite=Lax`.
- Uso de UUID en llaves primarias para prevenir enumeración de IDs.

### Detalle de seguridad

- Las contraseñas no se almacenan en texto plano.
- El sistema rota el refresh token y bloquea el anterior.
- Los OTP expiran en 5 minutos y sólo pueden usarse una vez.
- Las rutas administrativas y de auditoría están protegidas para usuarios `staff`.
- Las variables sensibles se cargan desde `.env`.

## 🧾 Auditoría

### Objetivo

Registrar eventos críticos con trazabilidad forense, análisis estadístico y cumplimiento de buenas prácticas.

### Tabla de auditoría

- `id`: UUID primario.
- `user_id`: referencia al usuario (nullable).
- `action`: código de la acción ejecutada.
- `severity`: nivel de criticidad (`INFO`, `WARNING`, `CRITICAL`).
- `ip_address`: dirección IP del cliente.
- `user_agent`: navegador/dispositivo.
- `metadata`: JSON con contexto adicional.
- `timestamp`: marca de tiempo automática.

### Acciones auditadas

- Autenticación: `LOGIN_SUCCESS`, `LOGIN_FAILED`, `LOGIN_OTP_SENT`, `LOGOUT`, `ACCOUNT_LOCKED`
- Chatbot: `CHAT_QUERY`, `CHAT_VOICE_QUERY`
- Acceso a datos académicos: `DATA_ACCESS_GRADES`, `DATA_ACCESS_SCHEDULE`, `DATA_ACCESS_PROFILE`
- RAG: `RAG_QUERY`, `RAG_INDEX_BUILD`
- Errores: `SYSTEM_ERROR`

### Índices de auditoría

- `user + timestamp`
- `action + timestamp`
- `severity + timestamp`

### Ventajas de esta auditoría

- Permite reconstruir el flujo de acciones de cada usuario.
- Soporta análisis estadístico por acción, severidad y periodo.
- Facilita el cumplimiento de requisitos de seguridad y de tesis.

## 📡 Endpoints principales

### Autenticación
- `POST /api/auth/login/`
- `POST /api/auth/verify-otp/`
- `POST /api/auth/logout/`
- `GET /api/auth/profile/`

### Estudiantes
- `GET /api/students/profile/`
- `GET /api/students/grades/`
- `GET /api/students/schedule/`
- `GET /api/students/stats/`
- `GET /api/students/notifications/`
- `POST /api/students/notifications/{id}/read/`
- `GET /api/students/activities/`
- `POST /api/students/activities/{id}/submit/`

### Docentes
- `GET /api/students/teacher/subjects/`
- `GET /api/students/teacher/schedule/`
- `GET /api/students/teacher/activities/`
- `POST /api/students/teacher/activities/`

### Chatbot
- `POST /api/chat/`
- `GET /api/chat/history/`
- `GET /api/chat/sessions/`

### Voz
- `POST /api/voice/stt/`
- `POST /api/voice/chat/`

### RAG
- `POST /api/rag/build/`
- `POST /api/rag/search/`

### Auditoría
- `GET /api/logs/`

## 🔧 Scripts útiles

- `python scripts/seed_database.py`
- `python scripts/seed_activities.py`
- `python scripts/rebuild_rag_index.py`
- `python scripts/scrape_rag_links.py`

## 🚀 Cómo iniciar el servidor local

1. Asegúrate de tener Python 3.11 instalado.
2. Activa el entorno virtual: `venv\Scripts\activate` (Windows) o `source venv/bin/activate` (Mac/Linux).
3. Instala dependencias: `pip install -r requirements.txt`.
4. Copia `.env.example` a `.env` y configura tus credenciales (`OPENAI_API_KEY`, `DJANGO_SECRET_KEY`, `DB_*`).
5. Ejecuta las migraciones: `python manage.py migrate`.
6. Arranca el servidor: `python manage.py runserver`.
7. La API estará disponible en `http://localhost:8000/`.
