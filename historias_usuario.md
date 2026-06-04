# Documento de Historias de Usuario - Tesis PUCESI

**Proyecto:** Prototipo de Chatbot Académico Inteligente con RAG  
**Autor:** Nick Bryan López Reina  
**Metodología:** Scrum

Este documento detalla las Historias de Usuario (HU) que definen las funcionalidades del sistema, siguiendo el formato estándar de la industria. A continuación se presentan las historias agrupadas por épicas, las tablas de sprints y el desglose de tareas para cada sprint.

---

## Historias de Usuario

### Épica 1: Autenticación y Seguridad
| ID | Título | Descripción | Criterios de Aceptación |
|:---|:---|:---|:---|
| **HU-01** | Autenticación Multi-Factor (MFA) | Como estudiante, quiero iniciar sesión con un código TOTP dinámico para que mi información académica esté protegida. | 1. El sistema valida código de estudiante y contraseña. <br> 2. Se solicita código de 6 dígitos. <br> 3. El login falla si el OTP es incorrecto. |
| **HU-02** | Registro de Auditoría | Como administrador, quiero que todos los accesos al chatbot queden registrados para cumplir con la trazabilidad de seguridad. | 1. Se guarda IP, usuario y marca de tiempo. <br> 2. El log es inmutable desde la interfaz de usuario. |

### Épica 2: Dashboard e Información Académica
| ID | Título | Descripción | Criterios de Aceptación |
|:---|:---|:---|:---|
| **HU-03** | Dashboard Dinámico (Escala 50/200) | Como estudiante, quiero ver mi promedio y asistencia calculados sobre la base de 200 puntos (3 parciales de 50 y examen de 50) para estar al día con mi rendimiento. | 1. El promedio se calcula sobre 200. <br> 2. Se muestra el % de asistencia actual. <br> 3. Los datos provienen del backend en tiempo real. |
| **HU-04** | Kardex con Filtros de Periodo | Como estudiante, quiero filtrar mis materias por semestre para revisar de forma ordenada mi historial académico pasado. | 1. Selector de periodo (ej. 2023-I). <br> 2. La tabla muestra profesor, aula y notas de ese periodo. <br> 3. El filtro se reinicia a "Todos" al entrar. |
| **HU-05** | Calendario de Clases | Como estudiante, quiero visualizar mi horario del semestre actual organizado por días de la semana para planificar mi asistencia. | 1. Muestre las 6 materias del nivel actual. <br> 2. Los días "MON", "TUE", etc., se traducen a nombres amigables. |

### Épica 3: Asistente Inteligente (Chatbot RAG)
| ID | Título | Descripción | Criterios de Aceptación |
|:---|:---|:---|:---|
| **HU-06** | Consulta Normativa (RAG) | Como estudiante, quiero preguntar sobre reglamentos universitarios y que el chatbot responda basándose en documentos oficiales. | 1. El bot consulta el índice vectorial de documentos. <br> 2. No alucina; si no está en el documento, indica que no sabe. |
| **HU-07** | Memoria Histórica Personalizada | Como estudiante, quiero preguntar sobre mis notas pasadas (ej: ¿quién me dio Programación en 1er semestre?) y que el bot responda correctamente. | 1. El bot accede al historial completo del estudiante. <br> 2. Responde en tiempo pasado para registros históricos. |
| **HU-08** | Interacción de Voz (V2V) | Como estudiante, quiero dictar mis dudas por voz y recibir respuestas habladas para facilitar la accesibilidad. | 1. El botón de micro activa la grabación. <br> 2. Se reproduce el audio de la respuesta automáticamente. |

---

## Historias de Usuario — Sprint 5: Seguridad, Auditoría y Endurecimiento

| ID | Nombre | Estimación (Días) | Importancia | Descripción de Historia de Usuario | Criterios de Aceptación | Dependencias |
|:---|:---|:---|:---|:---|:---|:---|
| S-5 | Acceso seguro al aula virtual | 10 | Alta | Como estudiante, quiero ingresar al aula virtual de forma segura para garantizar que mis credenciales, datos académicos y sesiones estén protegidos contra accesos no autorizados. | • Las contraseñas se almacenan con Argon2 (resistente a GPU/ASIC). <br> • El login requiere autenticación en dos factores (2FA) con código OTP de 6 dígitos vía email. <br> • La cuenta se bloquea automáticamente tras 5 intentos fallidos durante 15 minutos. <br> • Los tokens JWT tienen vida útil de 15 min (access) y 7 días (refresh) con rotación obligatoria. <br> • El Token Blacklist invalida tokens tras logout o rotación. <br> • Toda acción crítica (login, logout, consulta chatbot, acceso a notas) queda registrada en el Audit Log con IP, user-agent y timestamp. <br> • Las API aplican Rate Limiting (20 req/min anónimo, 100 req/min autenticado, 5 req/min login). <br> • La comunicación frontend-backend usa CORS restringido y cabeceras seguras (HttpOnly, SameSite). <br> • Los IDs de entidad usan UUIDv4 para evitar ataques de enumeración. | S-1, S-2, S-3, S-4 |

---

## Análisis y Refinamiento de Historias de Usuario (Tabla de Tareas por Sprint)

| Prioridad | Nro. Historia de Usuario | ID de Tarea | Tareas | Días (lunes-viernes, 4 horas) |
|:---|:---|:---|:---|:---|
| **Alta** | **1** | S-1-1 | Diseño de base de datos académica | 2 |
| | | S-1-2 | Configuración de PostgreSQL | 2 |
| | | S-1-3 | Desarrollo API REST académica | 2 |
| | | S-1-4 | Integración de horarios y asignaturas | 1 |
| | | S-1-5 | Implementación consulta de aulas | 1 |
| | | S-1-6 | Pruebas funcionales académicas | 2 |
| **Alta** | **2** | S-2-1 | Organización de documentos institucionales | 2 |
| | | S-2-2 | Configuración arquitectura RAG | 2 |
| | | S-2-3 | Implementación recuperación documental | 2 |
| | | S-2-4 | Integración con LLM | 2 |
| | | S-2-5 | Validación de respuestas institucionales | 2 |
| **Media** | **3** | S-3-1 | Implementación reconocimiento de voz | 2 |
| | | S-3-2 | Conversión Speech-to-Text | 2 |
| | | S-3-3 | Integración frontend voz | 2 |
| | | S-3-4 | Interpretación NLP de voz | 2 |
| | | S-3-5 | Pruebas multimodales | 2 |
| **Alta** | **4** | S-4-1 | Diseño interfaz conversacional React | 2 |
| | | S-4-2 | Gestión flujo de mensajes | 2 |
| | | S-4-3 | Manejo de estados y respuestas | 2 |
| | | S-4-4 | Integración chatbot frontend | 2 |
| | | S-4-5 | Pruebas integrales UI/UX | 2 |
| **Alta** | **5** | S-5-1 | Implementación de hashing Argon2 y validadores de contraseña | 2 |
| | | S-5-2 | Configuración de autenticación JWT (Access Token 15 min, Refresh 7 días, Blacklist, Rotación) | 2 |
| | | S-5-3 | Implementación de 2FA con OTP vía email (generación, envío, validación y expiración) | 2 |
| | | S-5-4 | Bloqueo automático de cuentas tras 5 intentos fallidos y desbloqueo temporizado (15 min) | 1 |
| | | S-5-5 | Implementación de Rate Limiting / Throttling en endpoints críticos (login, API, chatbot) | 1 |
| | | S-5-6 | Registro de auditoría (AuditLog): modelo, servicio centralizado y niveles de severidad (ISO 27001) | 2 |
| | | S-5-7 | Dashboard de estadísticas de auditoría y endpoint de consulta de logs para administradores | 1 |
| | | S-5-8 | Configuración de CORS, cabeceras seguras (HttpOnly, SameSite, CSRF) y protección XSS/Clickjacking | 1 |
| | | S-5-9 | Uso de UUIDv4 como llaves primarias y variables de entorno (.env) para secretos | 1 |
| | | S-5-10 | Pruebas integrales de seguridad y auditoría (penetración básica, validación de logs, simulación de ataques) | 2 |

---

*Una vez definido el conjunto de tareas, se procedió a su organización en Sprints, tomando en cuenta las dependencias y la capacidad del equipo.*
