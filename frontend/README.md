# 💻 Frontend (React + Vite) - Chatbot PUCE-SI

Este directorio contiene la aplicación cliente construida en React y TypeScript, empaquetada con Vite para un rendimiento ultrarrápido y una experiencia de usuario moderna.

## 📊 Resumen estadístico del frontend

- 6 páginas principales: `LandingPage`, `LoginPage`, `Dashboard`, `TeacherDashboard`, `AutoServicioBannerPage`, `BolsaEmpleoPage`
- 3 componentes clave: `ChatWindow`, `CampusMapSection`, `ProtectedRoute`
- 1 servicio API central: `src/services/api.ts`
- 1 store de autenticación: `src/store/authStore.ts`
- 1 widget flotante de chatbot con estados cerrado y abierto

## 🎨 Diseño y experiencia de usuario

El frontend usa **Tailwind CSS** y un diseño pensado para estudiantes. Sus atributos principales son:

- **Glassmorphism** en elementos de tarjeta y ventanas.
- **Dark mode** y contrastes definidos para lectura cómoda.
- **Responsive design** para mobile, tablet y desktop.
- **Animaciones suaves** con `framer-motion`.

## 🧠 Interfaz del chatbot flotante

El chatbot es un widget flotante que se adapta al diseño actual.

### Estado cerrado

- Un botón circular blanco fijo en la esquina inferior derecha.
- Borde suave y sombra pronunciada.
- Logo de PUCE visible dentro del botón.
- Representa la UI base con el chatbot inactivo.
- Mantiene el fondo principal de la página intacto, mostrando la interfaz general como imagen de referencia.

### Estado abierto

- Panel desplegable en la esquina inferior derecha.
- Header azul con logo PUCE, nombre `AcadBot PUCESI` y indicador de modo.
- Botón de cierre `X` para regresar al estado cerrado.
- Área de mensajes con burbujas:
  - Usuario a la derecha en azul.
  - Asistente a la izquierda en blanco.
- Indicador de carga / escritura.
- Entrada de texto y botones de voz y envío.
- Pie de panel con mensaje `Desarrollado para PUCE Sede Ibarra`.
- El panel se sobrepone al mismo fondo de la página, manteniendo la continuidad del diseño.

## 📷 Figuras para tesis

### Figura 1: Chatbot cerrado

Muestra la interfaz principal actual del frontend con el chatbot en reposo.
- Fondo: pantalla de la aplicación tal como se ve en el diseño.
- En la esquina inferior derecha aparece solo el botón flotante cerrado.
- Es ideal para ilustrar el estado inicial del widget antes de la interacción.

### Figura 2: Chatbot abierto

Muestra el mismo fondo de la interfaz principal con el chatbot desplegado.
- El panel del chatbot se abre sobre el contenido principal.
- Incluye el header azul, el historial de mensajes, la entrada de texto y los botones de voz/enviar.
- Permite comparar claramente el estado inactivo y activo del widget.

## 🧱 Estructura del frontend

### Componentes principales

- `src/components/ChatWindow.tsx`: Widget flotante del chatbot con envío de texto, grabación de voz y reproducción de audio.
- `src/components/CampusMapSection.tsx`: Mapa visual del campus con edificios, accesos temporales, aulas, servicios frecuentes y enlace a horarios/prerrequisitos 2026-01.
- `src/components/ProtectedRoute.tsx`: Protege rutas del dashboard para usuarios autenticados.
- `src/pages/Dashboard.tsx`: Panel central del estudiante con notificaciones, horario y calificaciones.
- `src/pages/TeacherDashboard.tsx`: Panel docente para materias, horario y carga de actividades.
- `src/pages/LandingPage.tsx`: Página pública con acceso al chatbot.
- `src/pages/LoginPage.tsx`: Interfaz de inicio de sesión.
- `src/pages/AutoServicioBannerPage.tsx` y `src/pages/BolsaEmpleoPage.tsx`: Páginas informativas.

### Servicios

- `src/services/api.ts`: Cliente HTTP unificado para consumir la API del backend.
- `src/store/authStore.ts`: Estado global de autenticación del estudiante.

### Integración del widget de chat

El widget se basa en las siguientes variables de estado:

- `isOpen`: controla apertura/cierre del panel.
- `messages`: historial de conversación.
- `input`: texto del usuario.
- `loading`: espera de respuesta.
- `isRecording`: estado de grabación de voz.

Soporta interacción por:
- texto
- voz
- notificaciones proactivas (cuando el usuario no es público y tiene mensajes pendientes)

## 📡 Endpoints consumidos por el frontend

- `POST /api/auth/login/`
- `POST /api/auth/verify-otp/`
- `GET /api/auth/profile/`
- `GET /api/students/profile/`
- `GET /api/students/grades/`
- `GET /api/students/schedule/`
- `GET /api/students/stats/`
- `GET /api/students/notifications/`
- `GET /api/students/activities/`
- `GET /api/students/teacher/subjects/`
- `GET /api/students/teacher/schedule/`
- `GET|POST /api/students/teacher/activities/`
- `POST /api/chat/`
- `POST /api/voice/chat/`

## 🔊 Funcionalidad de voz

- Usa `navigator.mediaDevices.getUserMedia({ audio: true })` para grabar.
- Envía audio en `multipart/form-data` a `/api/voice/chat/`.
- Reproduce respuestas de voz cuando el backend devuelve `audio_base64`.
- Detiene cualquier audio anterior antes de reproducir una nueva respuesta para evitar respuestas superpuestas.
- Maneja el cambio visual del botón de micrófono durante la grabación.

## 🚀 Cómo iniciar el entorno de desarrollo

1. Asegúrate de tener **Node.js** instalado (versión 18+ recomendada).
2. Abre una terminal en este directorio (`frontend/`).
3. Instala los paquetes:
   ```bash
   npm install
   ```
4. Configura la URL del backend en `.env` si es necesario.
5. Levanta el servidor local:
   ```bash
   npm run dev
   ```
6. El proyecto estará disponible en `http://localhost:5173/`.
