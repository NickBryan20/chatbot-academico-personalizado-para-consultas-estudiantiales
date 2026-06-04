# 📖 Metodología, Diseño y Desarrollo del Sistema (Capítulo para Tesis)

Este documento detalla exhaustivamente el marco de trabajo, la arquitectura, el diseño de la base de datos, los casos de uso y la ingeniería de Procesamiento de Lenguaje Natural (NLP) detrás del Chatbot Académico IA para la PUCE-SI. Además, incluye el código de los diagramas (en sintaxis PlantUML / PlantText) listos para ser renderizados e incluidos en el documento de tesis final.

---

## 1. Secuencia por Fases de Desarrollo

El desarrollo del sistema se estructuró bajo un enfoque iterativo y ágil, dividido en las siguientes fases críticas:

1. **Fase de Análisis y Modelado:** Levantamiento de requerimientos, diseño de la base de datos y flujos de usuario.
2. **Fase de Backend y RAG:** Construcción de la API en Django, implementación de FAISS, integración con OpenAI, y Web Scraping.
3. **Fase de Frontend y UI:** Desarrollo de la SPA en React (TailwindCSS, Glassmorphism).
4. **Fase de Integración y Seguridad:** Inyección de contexto al chatbot, JWT, Argon2, e implementación de Auditoría (ISO 27001).

A continuación, se detalla el diagrama de secuencia individual de cada fase.

### 1.1 Diagrama de Secuencia: Fase de Análisis y Modelado
```plantuml
@startuml
title Secuencia: Fase 1 - Análisis y Modelado
actor "Investigador / Tesista" as Tesista
participant "PUCE-SI" as Stakeholder
participant "Diseño Lógico" as Diseño

Tesista -> Stakeholder: Entrevista / Toma de Requerimientos
Stakeholder --> Tesista: Necesidad: Unificar Notas + Chatbot
Tesista -> Diseño: Elaboración de Casos de Uso
Diseño -> Diseño: Diseño del Modelo Relacional (ERD)
Diseño --> Tesista: Aprobación de Arquitectura
@enduml
```

### 1.2 Diagrama de Secuencia: Fase de Backend y RAG
```plantuml
@startuml
title Secuencia: Fase 2 - Backend y RAG
participant "Django API" as Backend
participant "Web Scraper" as Scraper
database "PostgreSQL / SQLite" as DB
database "FAISS Vector DB" as RAG

Backend -> DB: Ejecuta Migraciones y Tablas
Backend -> Scraper: Inicia scrape_rag_links.py
Scraper -> Scraper: Extrae URLs PUCE-SI
Scraper --> Backend: Retorna scraped_web_content.txt
Backend -> RAG: Genera Embeddings (OpenAI) y guarda Chunks
RAG --> Backend: FAISS Index Listo
@enduml
```

### 1.3 Diagrama de Secuencia: Fase de Frontend y UI
```plantuml
@startuml
title Secuencia: Fase 3 - Frontend UI/UX
participant "Desarrollador" as Dev
participant "Vite + React" as React
participant "TailwindCSS" as CSS
participant "Componentes" as UI

Dev -> React: Inicialización de Proyecto
React -> CSS: Configuración Tailwind y Dark Mode
Dev -> UI: Creación de Dashboard.tsx
Dev -> UI: Creación de ChatWidget.tsx
UI -> UI: Implementación Glassmorphism
UI --> Dev: UI Renderizada Correctamente
@enduml
```

### 1.4 Diagrama de Secuencia: Fase de Integración y Seguridad
```plantuml
@startuml
title Secuencia: Fase 4 - Integración y Seguridad
actor "Estudiante" as Estudiante
participant "React Frontend" as Frontend
participant "Middleware Auth (JWT)" as Auth
participant "Backend Django" as Backend
participant "Servicio Auditoría" as Audit

Estudiante -> Frontend: Ingresa Credenciales
Frontend -> Auth: POST /api/token/
Auth -> Auth: Verifica Argon2 Hash
Auth --> Frontend: Retorna Access Token JWT
Estudiante -> Frontend: Consulta Chatbot
Frontend -> Backend: Request Autenticado + JWT
Backend -> Audit: Registra 'CHAT_QUERY' con IP
Backend --> Frontend: Respuesta Procesada
@enduml
```

---

## 2. Arquitectura de Software

La aplicación sigue una **Arquitectura Cliente-Servidor Desacoplada** basada en micro-servicios lógicos. El Frontend consume el Backend exclusivamente a través de una API RESTful, lo que asegura escalabilidad independiente.

**Diagrama de Arquitectura (Código PlantText):**
```plantuml
@startuml
title Arquitectura del Sistema Chatbot PUCE-SI

node "Cliente (Estudiante)" {
  [React Frontend (SPA)] as React
  [Vite + TailwindCSS] as UI
  React --> UI
}

node "Servidor Backend (Django)" {
  [API REST Framework] as API
  [Chatbot Service] as Chatbot
  [RAG Engine] as RAG
  [Estudiantes Controller] as Auth
  [Audit Service] as Audit
  
  API --> Chatbot
  API --> Auth
  API --> Audit
  Chatbot --> RAG
  Chatbot --> Auth : "Solicita Contexto"
}

database "PostgreSQL / SQLite" {
  [Tablas Relacionales] as DB
}

database "FAISS Vector DB" {
  [Índice de Embeddings] as Vectores
}

cloud "OpenAI Cloud" {
  [GPT-4o / Whisper] as LLM
}

React <--> API : HTTP/JSON (JWT)
Auth <--> DB : Lectura/Escritura
Audit --> DB : Logs
RAG <--> Vectores : Búsqueda Semántica
Chatbot <--> LLM : "Prompt + Contexto"
@enduml
```

---

## 3. Casos de Uso y Alcance Funcional

El sistema contempla dos actores principales: el **Estudiante** (Usuario Final) y el **Administrador** (Auditor).

**Alcance Funcional del Estudiante:**
- Consultar horarios, calificaciones y subir deberes (Dashboard).
- Consultar al chatbot por voz o texto sobre temas académicos personales.
- Consultar información institucional pública (sin iniciar sesión).

**Diagrama de Casos de Uso (Código PlantText):**
```plantuml
@startuml
left to right direction
actor "Estudiante Autenticado" as Estudiante
actor "Visitante Público" as Visitante
actor "Administrador" as Admin

package "Chatbot Académico PUCE-SI" {
  usecase "Consultar Info Pública (RAG)" as UC1
  usecase "Consultar Notas y Horarios" as UC2
  usecase "Subir Tareas/Deberes" as UC3
  usecase "Hablar con Chatbot (Voz/Texto)" as UC4
  usecase "Auditar Uso de Chatbot" as UC5
}

Visitante --> UC1
Visitante --> UC4 : (Solo info general)

Estudiante --> UC1
Estudiante --> UC2
Estudiante --> UC3
Estudiante --> UC4 : (Info personalizada)

Admin --> UC5
@enduml
```

---

## 4. Base de Datos: Estructura y Relaciones

El sistema relacional fue diseñado con una alta normalización para evitar redundancia de datos. Las llaves primarias utilizan UUIDv4 para impedir ataques de enumeración.

**Diagrama Entidad-Relación (ERD) (Código PlantText):**
```plantuml
@startuml
title Diagrama Entidad-Relación (Base de Datos)
skinparam linetype ortho

entity "User" {
  id : UUID
  username : varchar
  password : varchar
  email : varchar
}

entity "Student" {
  id : UUID
  user_id : UUID <<FK>>
  student_code : varchar
  carrera : varchar
  semester_current : int
  career_start_date : date
}

entity "Professor" {
  id : UUID
  first_name : varchar
  last_name : varchar
  email : varchar
}

entity "Classroom" {
  id : UUID
  code : varchar
  building : varchar
  capacity : int
}

entity "Subject" {
  id : UUID
  code : varchar
  name : varchar
  credits : int
}

entity "Schedule" {
  id : UUID
  subject_id : UUID <<FK>>
  professor_id : UUID <<FK>>
  classroom_id : UUID <<FK>>
  day_of_week : varchar
  start_time : time
}

entity "Enrollment" {
  id : UUID
  student_id : UUID <<FK>>
  schedule_id : UUID <<FK>>
  academic_period : varchar
  status : varchar
}

entity "Grade" {
  id : UUID
  student_id : UUID <<FK>>
  subject_id : UUID <<FK>>
  final_grade : decimal
  attendance_percentage : decimal
}

entity "Activity" {
  id : UUID
  subject_id : UUID <<FK>>
  title : varchar
  due_date : datetime
}

entity "ActivitySubmission" {
  id : UUID
  student_id : UUID <<FK>>
  activity_id : UUID <<FK>>
  file : string
  status : varchar
}

entity "AuditLog" {
  id : UUID
  user_id : UUID <<FK>>
  action : varchar
  timestamp : datetime
}

entity "ConversationHistory" {
  id : UUID
  student_id : UUID <<FK>>
  message : text
}

User -- Student : 1 a 1
Student --> Grade : 1 a N
Subject --> Grade : 1 a N
Subject --> Schedule : 1 a N
Professor --> Schedule : 1 a N
Classroom --> Schedule : 1 a N
Student --> Enrollment : 1 a N
Schedule --> Enrollment : 1 a N
Subject --> Activity : 1 a N
Student --> ActivitySubmission : 1 a N
Activity --> ActivitySubmission : 1 a N
User --> AuditLog : 1 a N
Student --> ConversationHistory : 1 a N

@enduml
```

---

## 5. Base de Conocimiento del Sistema (RAG)

El RAG (Retrieval-Augmented Generation) resuelve el problema de la "desactualización" de la IA. El sistema mantiene su propia base de datos de conocimiento que lee automáticamente desde la web de la PUCE-SI.

**Diagrama de Flujo de Base de Conocimiento (Código PlantText):**
```plantuml
@startuml
title Flujo de Construcción de Base de Conocimiento (Web Scraping -> FAISS)

start
:Script de Scraping (`scrape_rag_links.py`);
:Leer URLs desde `puce_ibarra_info.txt`;
while (¿Quedan URLs pendientes?) is (Sí)
  :Petición HTTP GET;
  :BeautifulSoup limpia HTML;
  :Extraer Texto Puro (Carreras, Posgrados);
endwhile (No)
:Guardar en `scraped_web_content.txt`;
:Generar fragmentos (Chunks de 500 tokens);
:OpenAI `text-embedding-3-small`;
:Guardar vectores en Motor FAISS;
stop
@enduml
```

---

## 6. NLP (Procesamiento de Lenguaje Natural) y Diseño del Chatbot

El NLP del chatbot no recae en un modelo entrenado desde cero (Fine-Tuning), sino en la **Ingeniería de Prompts Contextuales**. Se utiliza el modelo GPT-4o-Mini por su bajo costo computacional y altísima precisión semántica.

**El "Prompt Maestro" Exacto utilizado en la configuración:**
```text
Eres el asistente académico oficial "AcadBot PUCESI".
REGLAS DE TIEMPO Y CONTEXTO:
1. Habla en PRESENTE para el periodo actual.
2. Habla en PASADO para cualquier periodo anterior.
3. Si el estudiante pregunta por detalles de semestres pasados, dáselos con precisión basándote en el HISTORIAL ACADÉMICO.
4. Jamás inventes datos. Si la info no está en el contexto, indícalo.
5. REGLA DE PRIVACIDAD ESTRICTA: Si el texto de documentos incluye detalles sobre 'DESCUENTOS Y BECAS', NO reveles esta info a menos que tengas el CONTEXTO DEL ESTUDIANTE AUTENTICADO.
6. Sé profesional, conciso y directo. RESPONDE EN MENOS DE 3 ORACIONES.
```

**Diagrama de Flujo de Consulta (NLP en Acción) (Código PlantText):**
```plantuml
@startuml
title Flujo de Resolución NLP de Preguntas

actor Estudiante
participant "React Frontend" as FE
participant "Django Backend" as BE
database "PostgreSQL" as DB
database "FAISS RAG" as RAG
participant "OpenAI (GPT-4o)" as IA

Estudiante -> FE: "¿Qué deberes tengo y cuánto cuesta alquilar aquí?"
FE -> BE: POST /api/chat/
BE -> DB: obtener_calificaciones() y obtener_actividades()
DB --> BE: [Retorna: Deber Matemáticas Pdte.]
BE -> RAG: Búsqueda Semántica ("alquiler")
RAG --> BE: [Retorna: "Departamentos cuestan $270"]
BE -> BE: Une Prompt Maestro + Notas DB + Texto RAG
BE -> IA: Request ChatCompletion
IA --> BE: Genera Respuesta Natural Combinada
BE -> FE: Respuesta de Texto JSON
FE -> Estudiante: Muestra Mensaje en Interfaz
@enduml
```

---

## 7. Diseño de la Interfaz Visual (UI/UX)

La interfaz fue diseñada con **React y TailwindCSS**, alejándose del diseño corporativo plano para adoptar un enfoque moderno para jóvenes universitarios:
1. **Glassmorphism:** Los contenedores del Dashboard tienen fondos translúcidos con desenfoque (blur), emulando vidrio esmerilado sobre un fondo degradado.
2. **Dark Mode Ergonómico:** Se utiliza un esquema de colores oscuros (slate/blue) que reduce la fatiga visual, ideal para estudiantes que acceden de noche.
3. **ChatWidget Flotante:** Permite al usuario hablar con el chatbot sin perder de vista la información del fondo (sus notas u horarios). Incluye retroalimentación háptica visual (animación de grabación del micrófono `lucide-react`).

**Diagrama de Jerarquía de Componentes (Código PlantText):**
```plantuml
@startuml
title Diseño de la Interfaz: Jerarquía de Componentes React

package "Aplicación React (Frontend)" {
  [Router Principal\n(App.tsx)] as App
  
  package "Páginas (Pages)" {
    [Vista Login] as Login
    [Vista Dashboard] as Dashboard
  }
  
  package "Componentes Reutilizables (UI)" {
    [Barra Lateral\n(Sidebar)] as Sidebar
    [Panel de Calificaciones] as Grades
    [Panel de Horarios] as Schedule
    [Modal de Tareas\n(ActivityModal)] as Modal
    [Widget de IA\n(ChatWindow)] as Chat
  }
}

App --> Login : "Ruta /"
App --> Dashboard : "Ruta /dashboard\n(Protegida)"

Dashboard --> Sidebar : "Navegación"
Dashboard --> Grades : "Renderiza"
Dashboard --> Schedule : "Renderiza"
Dashboard --> Modal : "Abrir Entrega"
Dashboard --> Chat : "Componente Flotante"

note bottom of Chat
  Contiene la lógica de
  reconocimiento de voz (Mic)
  y renderizado de Markdown.
end note
@enduml
```

### 7.1 Diseño del Chatbot Flotante — Estado Cerrado (Botón Circular)

El chatbot se presenta como un **botón flotante circular** posicionado en la esquina inferior derecha de la pantalla (`fixed bottom-8 right-8`). El botón contiene el logo institucional de la PUCE-SI y permanece visible en todo momento sobre cualquier página del sistema (Dashboard, Login público, etc.).

Al hacer clic en el botón, se despliega la ventana de conversación con una animación fluida (`framer-motion`: scale 0→1, opacity 0→1).

**Diagrama del Botón Flotante — Estado Cerrado (Código PlantText):**
```plantuml
@startuml
title Chatbot Flotante — Estado Cerrado (Botón de Activación)
skinparam backgroundColor #F8FAFC
skinparam defaultFontName Arial
skinparam defaultFontSize 11

rectangle "Pantalla del Navegador (Dashboard / Página Pública)" as Screen #E2E8F0 {

  rectangle "Barra Lateral\n(Sidebar)" as SB #334155 {
  }

  rectangle "Contenido Principal\n(Dashboard: Notas, Horarios, Tareas)" as Content #FFFFFF {
    rectangle "Panel de\nCalificaciones" as P1 #F1F5F9
    rectangle "Panel de\nHorarios" as P2 #F1F5F9
  }

}

' Botón flotante del chatbot
circle "  Logo\n PUCE  " as FAB #FFFFFF ##0033A0

note right of FAB #FFFDE7
  <b>Botón Flotante (FAB)</b>
  ────────────────────────
  • Posición: <b>fixed bottom-8 right-8</b>
  • Tamaño: <b>64x64 px</b> (w-16 h-16)
  • Fondo: <b>blanco</b> con sombra 2XL
  • Borde: <b>1px solid gray-100</b>
  • Contenido: Logo PUCE-SI (imagen)
  • Hover: <b>scale(1.10)</b>
  • Click: <b>scale(0.95)</b> → abre ventana
  • Z-index: <b>50</b>
  • Animación entrada: scale 0→1
    con framer-motion (delay 0.1s)
end note

' Flecha anotada señalando el botón
Content -[hidden]down-> FAB

@enduml
```

### 7.2 Diseño del Chatbot Flotante — Estado Abierto (Ventana de Conversación)

Al hacer clic en el botón flotante, se despliega una **ventana de chat** con dimensiones fijas de `384px de ancho × 580px de alto` (`w-96 h-[580px]`), que se superpone al contenido sin reemplazar la página. La ventana contiene tres zonas principales:

1. **Cabecera (Header):** Fondo azul institucional (#0033A0), logo PUCE en círculo blanco, nombre "AcadBot PUCESI", indicador de estado (punto verde pulsante), modo de operación ("Portal Estudiantil" o "Atención Pública") y botón de cerrar (X).

2. **Área de Mensajes:** Fondo gris claro (#F9FAFB), burbujas de usuario (azul celeste #00AEEF, alineadas a la derecha) y burbujas del asistente (blanco con borde, alineadas a la izquierda). Indicador de "escribiendo..." con 3 puntos animados (bounce).

3. **Área de Entrada:** Campo de texto redondeado, botón de micrófono (gris, se vuelve rojo pulsante al grabar) y botón de enviar (azul celeste #00AEEF). Pie de página "Desarrollado para PUCE Sede Ibarra".

**Diagrama de la Ventana de Chat — Estado Abierto (Código PlantText):**
```plantuml
@startuml
title Chatbot Flotante — Estado Abierto (Ventana de Conversación)
skinparam backgroundColor #F8FAFC
skinparam defaultFontName Arial
skinparam defaultFontSize 10

rectangle "Ventana del Chatbot\n(w-96 = 384px, h-[580px])\nfixed bottom-8 right-8\nz-index: 100\nborder-radius: 24px (rounded-3xl)\nshadow-2xl" as Window #FFFFFF {

  rectangle "<color:#FFFFFF><b>  ● Logo PUCE  |  AcadBot PUCESI</b>\n  <color:#90EE90>●</color> Portal Estudiantil           <color:#FFFFFF><b>✕</b></color></color>" as Header #0033A0

  rectangle "Área de Mensajes (flex-1, overflow-y-auto)" as MsgArea #F9FAFB {

    rectangle "<color:#FFFFFF>¿Cuáles son mis notas\n de Programación?</color>" as UserMsg1 #00AEEF

    rectangle "Según tu expediente, en\nProgramación I obtuviste\n168/200 (Aprobado)." as BotMsg1 #FFFFFF ##E5E7EB

    rectangle "<color:#FFFFFF>¿Qué deberes tengo\npendientes?</color>" as UserMsg2 #00AEEF

    rectangle "Tienes 1 deber pendiente:\nMatemáticas - Ejercicios\nCap. 5 (entrega: 15/Jun)." as BotMsg2 #FFFFFF ##E5E7EB

    rectangle "<color:#00AEEF>●  ●  ●</color>\n(escribiendo...)" as Typing #FFFFFF ##E5E7EB

  }

  rectangle "Área de Entrada (Input)" as InputArea #FFFFFF {
    rectangle "  Escribe tu consulta...                    " as InputField #F9FAFB ##E5E7EB
    circle " 🎤 " as MicBtn #F3F4F6
    circle " ➤ " as SendBtn #00AEEF
  }

  rectangle "<size:8><color:#9CA3AF>Desarrollado para PUCE Sede Ibarra</color></size>" as Footer #FFFFFF

}

note right of Header #E0F2FE
  <b>Header (Cabecera)</b>
  ─────────────────────
  • Fondo: <b>#0033A0</b> (azul PUCE)
  • Logo: círculo blanco 40x40px
  • Título: "AcadBot PUCESI" (bold)
  • Estado: punto verde pulsante
    (animate-pulse)
  • Modo: "Portal Estudiantil"
    o "Atención Pública"
  • Botón ✕: cierra la ventana
end note

note right of UserMsg1 #DBEAFE
  <b>Burbuja del Usuario</b>
  ─────────────────────
  • Fondo: <b>#00AEEF</b> (celeste)
  • Texto: <b>blanco</b>
  • Alineación: <b>derecha</b>
  • Border-radius: 16px
    (esquina sup-der: 2px)
  • max-width: 85%
end note

note right of BotMsg1 #F0FDF4
  <b>Burbuja del Asistente</b>
  ─────────────────────
  • Fondo: <b>blanco</b>
  • Borde: <b>1px gray-200</b>
  • Texto: <b>gray-800</b>
  • Alineación: <b>izquierda</b>
  • Border-radius: 16px
    (esquina sup-izq: 2px)
end note

note right of MicBtn #FEF2F2
  <b>Botón Micrófono</b>
  ─────────────────
  • Reposo: gris (#F3F4F6)
  • Grabando: <b>rojo (#EF4444)</b>
    + animate-pulse + scale(1.1)
  • Acción: mantener presionado
    (onMouseDown → onMouseUp)
  • Usa: MediaRecorder API
    + Whisper (OpenAI)
end note

note right of SendBtn #DBEAFE
  <b>Botón Enviar</b>
  ──────────────
  • Fondo: <b>#00AEEF</b>
  • Ícono: flecha (Send)
  • Disabled si: loading,
    grabando o input vacío
  • Hover: #0096CE
  • Click: scale(0.95)
end note

@enduml
```

### 7.3 Diagrama de Flujo de Interacción del Chatbot (Texto y Voz)

El siguiente diagrama muestra el flujo completo de interacción del usuario con el chatbot, tanto en modalidad de **texto** como de **voz**:

**Diagrama de Flujo de Interacción (Código PlantText):**
```plantuml
@startuml
title Flujo de Interacción del Chatbot Flotante (Texto y Voz)
skinparam activityBackgroundColor #FFFFFF
skinparam activityBorderColor #0033A0

start
:El estudiante ve el **botón flotante**
(círculo con logo PUCE, esquina inferior derecha);

:Hace **clic** en el botón flotante;
note right: Animación: scale 0→1\nopacity 0→1\n(framer-motion)

:Se abre la **ventana de chat**
(384×580px, rounded-3xl, shadow-2xl);

:Se muestra el **mensaje de bienvenida**:
"👋 ¡Hola! Soy el asistente inteligente
de la PUCE Ibarra";

if (¿Cómo desea interactuar?) then (Texto)
  :Escribe su consulta en el
  **campo de texto** (input);
  :Presiona **Enter** o el
  botón **Enviar** (➤);
  :Se muestra **burbuja azul** (usuario)
  alineada a la derecha;
else (Voz)
  :Mantiene presionado el
  botón **Micrófono** (🎤);
  note right: El botón cambia a\n**rojo pulsante**\n(animate-pulse)
  :El navegador activa
  **MediaRecorder API**;
  :Suelta el botón → se detiene
  la grabación;
  :Se envía el **audio (.webm)**
  al backend: POST /voice/chat/;
  :El backend transcribe con
  **OpenAI Whisper**;
  :Se muestra la **transcripción**
  como burbuja azul del usuario;
endif

:Se muestran **3 puntos animados**
(bounce) → "escribiendo...";

:El backend procesa la consulta:
1. Busca en **FAISS** (RAG)
2. Inyecta **contexto del estudiante**
3. Envía prompt a **GPT-4o-Mini**;

:Se recibe la respuesta del backend;

:Se muestra **burbuja blanca** (asistente)
alineada a la izquierda;

if (¿La respuesta incluye audio?) then (Sí)
  :Se reproduce automáticamente
  el **audio TTS** (base64→Audio);
endif

:El estudiante puede continuar
la conversación o **cerrar** (✕);

if (¿Cierra la ventana?) then (Sí)
  :La ventana se cierra con animación
  (y→100, scale→0.9, opacity→0);
  :Se vuelve a mostrar el
  **botón flotante** circular;
  stop
else (No)
  :Continúa escribiendo o
  grabando nuevas consultas;
  note right: El historial de mensajes\nse mantiene en el estado\nde React (useState)
endif

stop
@enduml
```

### 7.4 Diagrama de Wireframe del Chatbot — Vista General con Anotaciones

El siguiente diagrama presenta una vista general del comportamiento del chatbot en sus dos estados (cerrado y abierto) con flechas de transición:

```plantuml
@startuml
title Vista General: Transición del Chatbot Flotante (Cerrado → Abierto)
skinparam backgroundColor #FFFFFF
skinparam defaultFontName Arial
skinparam defaultFontSize 10

rectangle "ESTADO 1: CERRADO" as E1 {
  rectangle "Página Web (Dashboard)" as Page1 #F1F5F9 {
    rectangle "Sidebar" as SB1 #1E293B
    rectangle "Contenido\n(Notas / Horarios)" as C1 #FFFFFF
  }
  circle "Logo\nPUCE" as Btn #FFFFFF ##0033A0
  note bottom of Btn #FFFDE7
    <b>Botón FAB</b>
    64×64px
    Posición fija
    z-index: 50
  end note
}

rectangle "ESTADO 2: ABIERTO" as E2 {
  rectangle "Página Web (Dashboard)" as Page2 #F1F5F9 {
    rectangle "Sidebar" as SB2 #1E293B
    rectangle "Contenido\n(visible detrás)" as C2 #FFFFFF
  }
  rectangle "Ventana Chat" as Chat #FFFFFF ##0033A0 {
    rectangle "<b><color:#FFF>AcadBot PUCESI  ✕</color></b>" as H2 #0033A0
    rectangle "👋 ¡Hola! Soy el\nasistente de PUCE" as Msg #F9FAFB
    rectangle "[Escribe tu consulta...] 🎤 ➤" as In2 #FFFFFF ##E5E7EB
  }
  note bottom of Chat #E0F2FE
    <b>Ventana Chat</b>
    384×580px
    Posición fija
    z-index: 100
    rounded-3xl
  end note
}

Btn -right[#0033A0,bold]-> Chat : <b>Click</b>\n<color:#0033A0>Animación:\nscale(0→1)\nopacity(0→1)</color>

note top of E1 #F0FDF4
  El botón flotante está siempre
  visible sobre el contenido.
  No interfiere con la navegación.
end note

note top of E2 #FEF2F2
  La ventana de chat se superpone
  al contenido sin reemplazar la página.
  El usuario puede cerrarla con ✕.
end note

@enduml
```

---

## 8. Sprint 5: Seguridad, Auditoría y Endurecimiento del Sistema

### 8.1 Historia de Usuario del Sprint 5

**S-5 — Acceso seguro al aula virtual**

> *"Como estudiante, quiero ingresar al aula virtual de forma segura para garantizar que mis credenciales, datos académicos y sesiones estén protegidos contra accesos no autorizados."*

**Estimación:** 10 días (lunes a viernes, 4 horas/día)  
**Importancia:** Alta  
**Dependencias:** S-1, S-2, S-3, S-4

### 8.2 Desglose de Tareas del Sprint 5

| ID de Tarea | Tarea | Días | Detalle Técnico |
|:---|:---|:---|:---|
| S-5-1 | Implementación de hashing Argon2 y validadores de contraseña | 2 | Configurar `PASSWORD_HASHERS` con Argon2 como primario y PBKDF2 como fallback. Activar 4 validadores: similitud, longitud mínima (8), contraseñas comunes y numéricas puras. |
| S-5-2 | Configuración de autenticación JWT | 2 | Configurar `SimpleJWT` con Access Token de 15 min, Refresh de 7 días, rotación obligatoria (`ROTATE_REFRESH_TOKENS`), blacklist tras rotación, algoritmo HS256. |
| S-5-3 | Implementación de 2FA con OTP vía email | 2 | Crear modelo `OTPToken` con expiración de 5 min, servicio `OTPService` (generación de 6 dígitos, envío por email, invalidación de OTP anteriores), integración con el flujo de login. |
| S-5-4 | Bloqueo automático de cuentas | 1 | Implementar `increment_failed_attempts()` en el modelo `User`: bloqueo tras 5 intentos fallidos durante 15 minutos. Propiedad `is_locked` y método `reset_failed_attempts()`. |
| S-5-5 | Implementación de Rate Limiting | 1 | Configurar `DEFAULT_THROTTLE_RATES` en DRF: anónimo (20/min), autenticado (100/min), login (5/min). Aplicar `throttle_scope='login'` a las vistas de autenticación. |
| S-5-6 | Registro de auditoría (AuditLog) | 2 | Crear modelo `AuditLog` con 13 acciones, 3 niveles de severidad, campos IP/user-agent/metadata(JSON). Crear servicio `AuditLogService` centralizado con métodos especializados. Añadir 3 índices compuestos. |
| S-5-7 | Dashboard de auditoría para administradores | 1 | Crear `AuditLogListView` (paginación 50/página, filtros por acción/severidad) y `ChatbotUsageStatsView` (estadísticas con filtros de fecha/usuario). Permisos `IsAdminUser`. |
| S-5-8 | Configuración de CORS y cabeceras seguras | 1 | Configurar `CORS_ALLOWED_ORIGINS`, `SESSION_COOKIE_HTTPONLY`, `SESSION_COOKIE_SAMESITE=Lax`, `CSRF_COOKIE_SAMESITE=Lax`, middleware `SecurityMiddleware` y `XFrameOptionsMiddleware`. |
| S-5-9 | UUIDv4 y variables de entorno | 1 | Usar `uuid.uuid4` como PK en todas las tablas. Migrar todas las credenciales a `.env` con `python-decouple`. Crear `.env.example` documentado. |
| S-5-10 | Pruebas integrales de seguridad y auditoría | 2 | Validar: login con OTP, bloqueo por fuerza bruta, expiración de tokens, rotación de refresh, inmutabilidad de logs, throttling, CORS bloqueado desde origen no autorizado. |

### 8.3 Diagrama de Secuencia: Flujo de Autenticación Segura (JWT + 2FA)

```plantuml
@startuml
title Secuencia: Sprint 5 — Flujo de Autenticación Segura (JWT + 2FA + Argon2)

actor "Estudiante" as User
participant "React Frontend" as FE
participant "LoginView\n(Django)" as Login
participant "Argon2\nHasher" as Argon
participant "OTPService" as OTP
participant "Email SMTP" as Email
participant "OTPVerifyView" as Verify
participant "SimpleJWT" as JWT
participant "AuditLogService" as Audit
database "PostgreSQL" as DB

== Paso 1: Ingreso de Credenciales ==
User -> FE: Ingresa código de estudiante\ny contraseña
FE -> Login: POST /api/auth/login/\n{username, password}

Login -> Login: Verificar throttle_scope='login'\n(máx 5 req/min)
Login -> DB: Buscar usuario por username
DB --> Login: Usuario encontrado

Login -> Login: Verificar is_locked\n(¿account_locked_until > now?)
note right: Si está bloqueado:\nretorna 423 Locked\n+ registra ACCOUNT_LOCKED

Login -> Argon: check_password(password, hash)
Argon -> Argon: Ejecuta Argon2id\n(memory-hard, anti-GPU)
Argon --> Login: ✅ Contraseña válida

== Paso 2: Generación y Envío de OTP ==
Login -> OTP: generate_and_send(user)
OTP -> DB: Invalidar OTPs anteriores\n(is_used=True)
OTP -> OTP: Generar código de 6 dígitos\n(random.choices)
OTP -> DB: Crear OTPToken\n(code, expires_at=now+5min,\ntemp_token=UUID)
OTP -> Email: send_mail()\n"Tu código: 847291"
Email --> User: 📧 Email con código OTP

OTP -> Audit: log('LOGIN_OTP_SENT')
Login --> FE: {requires_2fa: true,\ntemp_token: "uuid..."}

== Paso 3: Verificación del OTP ==
User -> FE: Ingresa código OTP\n(6 dígitos)
FE -> Verify: POST /api/auth/verify-otp/\n{temp_token, otp_code}

Verify -> DB: Buscar OTPToken\npor temp_token
DB --> Verify: OTPToken encontrado

Verify -> Verify: Validar:\n• ¿is_used == false?\n• ¿expires_at > now?\n• ¿code coincide?

Verify -> OTP: mark_used(otp)
Verify -> DB: reset_failed_attempts()\n(contador = 0)

== Paso 4: Emisión de Tokens JWT ==
Verify -> JWT: RefreshToken.for_user(user)
JWT --> Verify: access_token (15 min)\n+ refresh_token (7 días)

Verify -> DB: Actualizar last_login_ip\ny last_login
Verify -> Audit: log('LOGIN_SUCCESS',\nmethod='2FA+OTP')

Verify --> FE: {access, refresh, user}
FE -> FE: Almacenar tokens\nen memoria/localStorage

== Paso 5: Peticiones Autenticadas ==
User -> FE: Consulta el chatbot
FE -> Login: Request con Header:\nAuthorization: Bearer <access_token>

@enduml
```

### 8.4 Diagrama de Secuencia: Flujo de Auditoría (ISO 27001)

```plantuml
@startuml
title Secuencia: Sprint 5 — Registro de Auditoría Centralizado (ISO 27001)

actor "Estudiante" as User
participant "React Frontend" as FE
participant "Django View\n(cualquier módulo)" as View
participant "AuditLogService" as Audit
database "Tabla audit_log\n(PostgreSQL)" as DB
participant "AdminView\n(Dashboard)" as Admin

== Evento: Consulta al Chatbot ==
User -> FE: Escribe pregunta al chatbot
FE -> View: POST /api/chat/\n{message: "¿Cuánto cuesta...?"}\nHeader: Authorization: Bearer xxx

View -> View: Procesar consulta\n(RAG + LLM)

View -> Audit: log_chat_query(\n  user=estudiante,\n  query="¿Cuánto cuesta...?",\n  response_preview="El costo es...",\n  tokens_used=347,\n  request=request\n)

Audit -> Audit: Extraer IP automáticamente:\nX-Forwarded-For o REMOTE_ADDR
Audit -> Audit: Extraer User-Agent\ndel request HTTP

Audit -> DB: INSERT INTO audit_log\n(id=UUID, user_id, action='CHAT_QUERY',\nseverity='INFO', ip_address='192.168.1.5',\nuser_agent='Mozilla/5.0...',\nmetadata={query_preview, response_preview,\ntokens_used}, timestamp=NOW())

note right of DB
  <b>Registro inmutable:</b>
  • No existe endpoint PUT/DELETE
    para modificar logs
  • Solo INSERT desde el servicio
  • Acceso de lectura: solo admins
end note

DB --> Audit: ✅ Log registrado
Audit --> View: Retorna AuditLog entry

View --> FE: Respuesta del chatbot

== Evento: Login Fallido ==
User -> FE: Ingresa contraseña incorrecta
FE -> View: POST /api/auth/login/

View -> Audit: log_login_failed(\n  user=estudiante,\n  reason="invalid_password",\n  request=request\n)

Audit -> DB: INSERT INTO audit_log\n(action='LOGIN_FAILED',\nseverity='WARNING',\nmetadata={reason, failed_attempts: 3})

== Consulta de Auditoría por Administrador ==
Admin -> View: GET /api/audit-logs/\n?action=LOGIN_FAILED\n&severity=WARNING
View -> DB: SELECT * FROM audit_log\nWHERE action='LOGIN_FAILED'\nAND severity='WARNING'\nORDER BY timestamp DESC\nLIMIT 50
DB --> View: Lista paginada de logs
View --> Admin: JSON con logs de auditoría

Admin -> View: GET /api/audit-logs/stats/\n?start_date=2026-01-01\n&end_date=2026-06-01
View -> DB: SELECT COUNT(*)\nFROM audit_log\nWHERE action='CHAT_QUERY'
DB --> View: total_queries: 1,247
View --> Admin: {total_queries: 1247}

@enduml
```

### 8.5 Diagrama de Arquitectura de Seguridad (Capas de Defensa)

```plantuml
@startuml
title Arquitectura de Seguridad en Capas (Defense in Depth)
skinparam componentStyle uml2
skinparam backgroundColor #FFFFFF

rectangle "Capa 1: Red y Transporte" as L1 #FFECB3 {
  [CORS Restrictivo\n(Solo orígenes autorizados)] as CORS
  [Cabeceras Seguras\n(HttpOnly, SameSite, X-Frame)] as Headers
  [Rate Limiting\n(Anón: 20/min, Auth: 100/min,\nLogin: 5/min)] as Throttle
}

rectangle "Capa 2: Autenticación" as L2 #BBDEFB {
  [Argon2 Hashing\n(Memory-hard, anti-GPU)] as Hash
  [JWT Tokens\n(Access: 15min, Refresh: 7d,\nRotación + Blacklist)] as JWTComp
  [2FA / OTP\n(6 dígitos, 5min expiración,\nenvío por email)] as TwoFA
  [Bloqueo de Cuentas\n(5 intentos → 15min lock)] as Lock
}

rectangle "Capa 3: Autorización" as L3 #C8E6C9 {
  [Permisos por Rol\n(IsAuthenticated,\nIsAdminUser)] as Perms
  [Rutas Protegidas\n(ProtectedRoute en React)] as Routes
}

rectangle "Capa 4: Datos" as L4 #E1BEE7 {
  [UUIDv4 como PKs\n(Anti-enumeración)] as UUID
  [Variables de Entorno\n(.env con python-decouple)] as ENV
  [Validadores de Contraseña\n(4 reglas de complejidad)] as PWValid
}

rectangle "Capa 5: Auditoría y Monitoreo" as L5 #FFCDD2 {
  [AuditLog Service\n(13 acciones, 3 severidades,\nIP + User-Agent + Metadata)] as AuditSvc
  [Índices Compuestos\n(user+ts, action+ts,\nseverity+ts)] as Indexes
  [Dashboard Admin\n(Logs paginados +\nEstadísticas de uso)] as Dashboard
}

L1 -[hidden]down-> L2
L2 -[hidden]down-> L3
L3 -[hidden]down-> L4
L4 -[hidden]down-> L5

note right of L1
  **Primera línea de defensa:**
  Filtra peticiones maliciosas
  antes de llegar al código.
end note

note right of L2
  **Verificación de identidad:**
  Multi-factor con criptografía
  robusta y protección anti-bruta.
end note

note right of L5
  **Trazabilidad forense:**
  Cumple ISO 27001 para
  no repudio e inmutabilidad.
end note

@enduml
```

### 8.6 Tabla Resumen de Controles de Seguridad Implementados

| # | Control | Norma/Estándar | Archivo en el Código | Línea Aprox. |
|:---|:---|:---|:---|:---|
| 1 | Hashing Argon2 | OWASP, PHC 2015 | `backend/config/settings/base.py` | 104 |
| 2 | Validadores de contraseña (4) | OWASP | `backend/config/settings/base.py` | 95 |
| 3 | JWT con rotación y blacklist | RFC 7519, OAuth 2.0 | `backend/config/settings/base.py` | 147 |
| 4 | 2FA / OTP por email | ISO 27001 A.9.4.2 | `backend/apps/authentication/services.py` | 18 |
| 5 | Bloqueo por intentos fallidos | ISO 27001 A.9.4.3 | `backend/apps/authentication/models.py` | 48 |
| 6 | Rate Limiting (3 niveles) | OWASP API Security | `backend/config/settings/base.py` | 132 |
| 7 | CORS restrictivo | OWASP | `backend/config/settings/base.py` | 163 |
| 8 | Cookies HttpOnly + SameSite | OWASP | `backend/config/settings/base.py` | 217 |
| 9 | X-Frame-Options (Clickjacking) | OWASP | `backend/config/settings/base.py` | Middleware |
| 10 | UUIDv4 como PKs | OWASP (IDOR) | Todos los modelos | Línea `id = models.UUIDField(...)` |
| 11 | Variables de entorno (.env) | 12-Factor App | `backend/config/settings/base.py` | 13 |
| 12 | AuditLog (13 acciones) | ISO 27001 A.12.4 | `backend/apps/audit_logs/models.py` | 9 |
| 13 | Servicio centralizado de auditoría | ISO 27001 A.12.4 | `backend/apps/audit_logs/services.py` | 13 |
| 14 | Dashboard de auditoría (admin) | ISO 27001 A.12.4 | `backend/apps/audit_logs/views.py` | 12 |
