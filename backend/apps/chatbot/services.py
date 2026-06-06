"""
Servicio del Chatbot: pipeline completo de generación de respuestas.
Integra: datos académicos del estudiante + RAG + OpenAI LLM.
El sistema NO genera información inventada.
"""
import logging
import re
from datetime import timedelta
from typing import Optional

from django.conf import settings
from django.utils import timezone
import httpx

from ..students.models import Student, Grade, Schedule, Enrollment, ConversationHistory
from ..rag.engine import rag_engine
from ..audit_logs.services import AuditLogService

logger = logging.getLogger(__name__)

SPANISH_WEEKDAYS = [
    'lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo'
]
SPANISH_MONTHS = [
    '', 'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
    'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'
]

WEATHER_LOCATIONS = {
    'ibarra': (0.3517, -78.1223, 'Ibarra, Ecuador'),
    'quito': (-0.1807, -78.4678, 'Quito, Ecuador'),
    'guayaquil': (-2.1894, -79.8891, 'Guayaquil, Ecuador'),
    'cuenca': (-2.9006, -79.0045, 'Cuenca, Ecuador'),
    'loja': (-3.9931, -79.2042, 'Loja, Ecuador'),
    'ambato': (-1.2543, -78.6229, 'Ambato, Ecuador'),
    'manta': (-0.9677, -80.7089, 'Manta, Ecuador'),
    'tulcan': (0.8119, -77.7173, 'Tulcán, Ecuador'),
    'otavalo': (0.2346, -78.2625, 'Otavalo, Ecuador'),
    'cayambe': (0.0411, -78.1457, 'Cayambe, Ecuador'),
}

WEATHER_CODE_DESCRIPTIONS = {
    0: 'cielo despejado',
    1: 'mayormente despejado',
    2: 'parcialmente nublado',
    3: 'nublado',
    45: 'neblina',
    48: 'neblina con escarcha',
    51: 'llovizna ligera',
    53: 'llovizna moderada',
    55: 'llovizna intensa',
    61: 'lluvia ligera',
    63: 'lluvia moderada',
    65: 'lluvia intensa',
    80: 'chubascos ligeros',
    81: 'chubascos moderados',
    82: 'chubascos fuertes',
    95: 'tormenta',
    96: 'tormenta con granizo ligero',
    99: 'tormenta con granizo fuerte',
}

SYSTEM_PROMPT = """Eres el asistente académico oficial "AcadBot PUCESI".
REGLAS DE TIEMPO Y CONTEXTO:
1. Habla en PRESENTE para el periodo actual.
2. Habla en PASADO para cualquier periodo anterior.
3. Si el estudiante pregunta por detalles de semestres pasados, dáselos con precisión basándote en el HISTORIAL ACADÉMICO.
4. Jamás inventes datos. Si la info no está en el contexto, indícalo.
5. REGLA DE PRIVACIDAD ESTRICTA: Si el texto de documentos institucionales incluye detalles sobre 'DESCUENTOS Y BECAS ESPECIALES 2026', NO reveles esta información a menos que tengas el CONTEXTO ACADÉMICO DEL ESTUDIANTE AUTENTICADO. Si eres el chatbot público (no tienes contexto de estudiante), responde amablemente que debe iniciar sesión.
6. Sé profesional, conciso y directo. RESPONDE EN MENOS DE 3 ORACIONES SIEMPRE QUE SEA POSIBLE.
7. CONTINUIDAD: Presta mucha atención al HISTORIAL DE CONVERSACIÓN. Si el usuario te hace una pregunta corta o de seguimiento (ej. "¿y dónde es eso?"), usa el contexto anterior para responder.
8. IDIOMA ESTRICTO: Responde ÚNICA Y EXCLUSIVAMENTE EN ESPAÑOL. Evita usar modismos o palabras en inglés (a menos que sea el nombre de una materia como 'English I'). Escribe los números y siglas de forma que un lector de voz automatizado pueda pronunciarlos fácilmente en español.
9. JERARQUÍA RAG: Si hay conflicto entre documentos validados del proyecto y contenido web, usa los documentos validados para reglas académicas del prototipo (calificaciones, aula virtual, actividades y datos simulados). Usa la web oficial de PUCE-SI para información pública cambiante como admisiones, oferta académica, horarios publicados y preguntas frecuentes.
10. CAMPUS Y CALIFICACIONES: Para ubicación de aulas, edificios, biblioteca, bar/cafetería, copias, tesorería, secretaría y carnet institucional, consulta primero el mapa de campus validado. El carnet institucional se gestiona en el Edificio 2, piso 3. Para ingresar físicamente al campus, el estudiante debe presentar su carnet estudiantil vigente; si no lo porta, debe registrar su ingreso en la hoja de control administrada por los guardias de seguridad. Para calificaciones, usa la regla del prototipo: 4 componentes de 50 puntos, mínimo 30/50 por componente, 120/200 total y 80% de asistencia.
11. HORARIOS Y PRERREQUISITOS: Si el estudiante autenticado pregunta por "mi horario", usa su contexto académico de base de datos. Si pregunta por horarios oficiales, prerrequisitos, NRC o PDFs por carrera del periodo 2026-01, usa la página oficial de Horarios Estudiantiles 2026-01 y no inventes prerrequisitos específicos.
12. FECHA, HORA Y CLIMA: Usa siempre el CONTEXTO OPERATIVO DEL SISTEMA para responder preguntas sobre hoy, ayer, mañana, hora actual o clima. No digas que no tienes acceso a la fecha si el contexto la incluye.
"""


class ChatbotService:
    """Pipeline completo del chatbot académico con RAG."""

    def __init__(self):
        self._client = None

    def get_client(self):
        """Inicializa el cliente OpenAI de forma lazy."""
        if self._client is None:
            from openai import OpenAI
            self._client = OpenAI(api_key=settings.OPENAI_API_KEY)
        return self._client

    def _format_date_es(self, value) -> str:
        weekday = SPANISH_WEEKDAYS[value.weekday()]
        month = SPANISH_MONTHS[value.month]
        return f"{weekday}, {value.day} de {month} de {value.year}"

    def get_system_context(self) -> str:
        """Contexto operativo no sensible disponible para chat público y privado."""
        now = timezone.localtime(timezone.now())
        today = now.date()
        yesterday = today - timedelta(days=1)
        tomorrow = today + timedelta(days=1)

        return "\n".join([
            "=== CONTEXTO OPERATIVO DEL SISTEMA ===",
            f"Zona horaria: {settings.TIME_ZONE}",
            f"Fecha actual: {self._format_date_es(today)}",
            f"Hora actual: {now.strftime('%H:%M')}",
            f"Ayer fue: {self._format_date_es(yesterday)}",
            f"Mañana será: {self._format_date_es(tomorrow)}",
            "Usa estos datos para resolver preguntas relativas como hoy, ayer, mañana, esta semana o la hora actual.",
        ])

    def _is_direct_time_query(self, message: str) -> bool:
        text = message.lower()
        compact = re.sub(r'[^\wáéíóúñ]+', ' ', text).strip()
        if compact in {'hoy', 'ayer', 'mañana', 'manana'}:
            return True

        academic_terms = {
            'clase', 'clases', 'horario', 'horarios', 'materia', 'materias',
            'asignatura', 'asignaturas', 'aula', 'aulas', 'profesor',
            'profesora', 'docente', 'docentes', 'actividad', 'actividades',
            'tarea', 'tareas', 'deber', 'deberes', 'entrega', 'entregas',
            'examen', 'examenes', 'nrc', 'universidad', 'campus', 'ingresar',
            'ingreso', 'entrar', 'entrada', 'acceder', 'acceso',
        }
        if academic_terms.intersection(compact.split()):
            return False

        has_date_word = any(word in text for word in ['fecha', 'día', 'dia'])
        has_time_word = 'hora' in text
        has_relative_word = any(word in text for word in ['hoy', 'ayer', 'mañana', 'manana', 'actual'])
        asks_current_day = bool(re.search(r'\b(día|dia)\s+estamos\b', text))
        asks_explicit_date = bool(re.search(r'\b(qué|que)\s+(fecha|día|dia)\b', text))
        asks_explicit_time = bool(re.search(r'\b(qué|que)\s+hora\s+(es|son)\b', text))

        return (
            asks_current_day
            or asks_explicit_date
            or asks_explicit_time
            or (has_date_word and has_relative_word)
            or (has_time_word and has_relative_word)
        )

    def _answer_time_query(self, message: str) -> Optional[str]:
        if not self._is_direct_time_query(message):
            return None

        now = timezone.localtime(timezone.now())
        text = message.lower()
        target_date = now.date()
        prefix = 'Hoy es'

        if 'ayer' in text:
            target_date = target_date - timedelta(days=1)
            prefix = 'Ayer fue'
        elif 'mañana' in text or 'manana' in text:
            target_date = target_date + timedelta(days=1)
            prefix = 'Mañana será'

        formatted_date = self._format_date_es(target_date)
        if 'hora' in text and not any(word in text for word in ['fecha', 'día', 'dia', 'ayer', 'mañana', 'manana']):
            return f"Son las {now.strftime('%H:%M')} en la zona horaria {settings.TIME_ZONE}."
        if 'hora' in text:
            return f"{prefix} {formatted_date}. La hora actual es {now.strftime('%H:%M')} en {settings.TIME_ZONE}."
        return f"{prefix} {formatted_date}."

    def _is_ambiguous_university_entry_query(self, message: str) -> bool:
        compact = re.sub(r'[^\wáéíóúñ]+', ' ', message.lower()).strip()
        words = set(compact.split())

        entry_terms = {'ingresar', 'ingreso', 'entrar', 'entrada', 'acceder', 'acceso'}
        university_terms = {'universidad', 'pucesi', 'puce', 'campus', 'institucion', 'institución'}
        admission_terms = {
            'admision', 'admisión', 'admisiones', 'postular', 'postulacion',
            'postulación', 'inscripcion', 'inscripción', 'requisito',
            'requisitos', 'matricula', 'matrícula', 'carrera', 'grado',
            'tecnologia', 'tecnología', 'posgrado', 'examen',
        }
        physical_entry_terms = {
            'fisico', 'físico', 'fisica', 'física', 'fisicamente',
            'físicamente', 'presencial', 'presencialmente', 'carnet',
            'credencial', 'guardia', 'guardias', 'garita', 'seguridad',
            'porton', 'portón', 'puerta', 'control', 'vehiculo', 'vehículo',
            'auto', 'carro', 'moto',
        }
        virtual_access_terms = {'virtual', 'plataforma', 'moodle', 'aula', 'aulas'}

        has_entry_intent = bool(entry_terms.intersection(words))
        has_university_scope = bool(university_terms.intersection(words))
        has_specific_intent = bool(
            admission_terms.intersection(words)
            or physical_entry_terms.intersection(words)
            or virtual_access_terms.intersection(words)
        )

        return has_entry_intent and has_university_scope and not has_specific_intent

    def _answer_university_entry_clarification(self, message: str) -> Optional[str]:
        if not self._is_ambiguous_university_entry_query(message):
            return None

        return (
            "Para orientarte correctamente, ¿te refieres al proceso de admisión "
            "y requisitos para ingresar como estudiante, o al ingreso físico al "
            "campus de la universidad?"
        )

    def _is_weather_query(self, message: str) -> bool:
        text = message.lower()
        return any(word in text for word in ['clima', 'temperatura', 'llueve', 'lluvia', 'pronóstico', 'pronostico'])

    def _weather_location_from_message(self, message: str) -> tuple[float, float, str]:
        normalized = message.lower()
        for key, location in WEATHER_LOCATIONS.items():
            if key in normalized:
                return location
        return (
            settings.WEATHER_DEFAULT_LATITUDE,
            settings.WEATHER_DEFAULT_LONGITUDE,
            settings.WEATHER_DEFAULT_LOCATION,
        )

    def _answer_weather_query(self, message: str) -> Optional[str]:
        if not self._is_weather_query(message):
            return None
        if not settings.WEATHER_ENABLED:
            return "La consulta de clima está deshabilitada temporalmente en el sistema."

        latitude, longitude, location_name = self._weather_location_from_message(message)
        try:
            response = httpx.get(
                'https://api.open-meteo.com/v1/forecast',
                params={
                    'latitude': latitude,
                    'longitude': longitude,
                    'current': (
                        'temperature_2m,relative_humidity_2m,apparent_temperature,'
                        'precipitation,rain,weather_code,cloud_cover,wind_speed_10m'
                    ),
                    'timezone': settings.TIME_ZONE,
                    'forecast_days': 1,
                },
                timeout=settings.WEATHER_TIMEOUT_SECONDS,
            )
            response.raise_for_status()
            current = response.json().get('current', {})
        except Exception as e:
            logger.warning("No se pudo consultar clima para %s: %s", location_name, e)
            return (
                f"No pude consultar el clima de {location_name} en este momento. "
                "Intenta nuevamente en unos minutos o revisa una fuente meteorológica oficial."
            )

        temperature = current.get('temperature_2m')
        feels_like = current.get('apparent_temperature')
        humidity = current.get('relative_humidity_2m')
        precipitation = current.get('precipitation')
        wind = current.get('wind_speed_10m')
        cloud_cover = current.get('cloud_cover')
        weather_code = current.get('weather_code')
        description = WEATHER_CODE_DESCRIPTIONS.get(weather_code, 'condición meteorológica no clasificada')
        observed_at = current.get('time')

        return (
            f"El clima actual en {location_name} es {description}, con {temperature} °C "
            f"(sensación térmica de {feels_like} °C), humedad del {humidity} %, "
            f"precipitación de {precipitation} mm, nubosidad del {cloud_cover} % "
            f"y viento de {wind} km/h. Datos actualizados por Open-Meteo"
            f"{f' a las {observed_at}' if observed_at else ''}."
        )

    def _direct_tool_response(self, message: str) -> Optional[dict]:
        clarification_response = self._answer_university_entry_clarification(message)
        if clarification_response:
            return {
                'response': clarification_response,
                'tokens_used': 0,
                'rag_sources': [],
                'tool_used': 'clarification',
            }

        weather_response = self._answer_weather_query(message)
        if weather_response:
            return {
                'response': weather_response,
                'tokens_used': 0,
                'rag_sources': [],
                'tool_used': 'weather',
            }

        time_response = self._answer_time_query(message)
        if time_response:
            return {
                'response': time_response,
                'tokens_used': 0,
                'rag_sources': [],
                'tool_used': 'system_time',
            }

        return None

    def get_student_context(self, student: Optional[Student]) -> str:
        """
        Construye el contexto académico del estudiante.
        Si no hay estudiante, retorna un string vacío.
        """
        if not student:
            return ""

        lines = [
            f"=== DATOS ACADÉMICOS DEL ESTUDIANTE AUTENTICADO ===",
            f"Nombre: {student.full_name}",
            f"Código estudiantil: {student.student_code}",
            f"Correo institucional: {student.email}",
            f"Carrera: {student.get_carrera_display()}",
            f"Semestre actual: {student.semester_current}",
            "",
        ]

        # 1. Obtener todas las notas e historial (Agrupado por Periodo)
        all_grades = Grade.objects.filter(student=student).select_related('subject').order_by('-academic_period', 'subject__semester')
        
        # Determinar el periodo actual basado en las notas o usar el defecto
        current_period = '2026-01'
        if all_grades.exists():
            current_period = all_grades.first().academic_period
            
        if all_grades.exists():
            lines.append("HISTORIAL ACADÉMICO COMPLETO:")
            current_grades = [g for g in all_grades if g.academic_period == current_period]
            past_grades = [g for g in all_grades if g.academic_period != current_period]
            
            if current_grades:
                lines.append(f"\n[PERIODO ACTUAL: {current_period}]")
                for grade in current_grades:
                    p1 = f"{grade.partial_1}/50" if grade.partial_1 is not None else "—"
                    p2 = f"{grade.partial_2}/50" if grade.partial_2 is not None else "—"
                    p3 = f"{grade.partial_3}/50" if grade.partial_3 is not None else "—"
                    exam = f"{grade.final_exam}/50" if grade.final_exam is not None else "—"
                    final = f"{grade.final_grade}/200" if grade.final_grade is not None else "En curso"
                    lines.append(f"  • {grade.subject.name}: P1={p1} | P2={p2} | P3={p3} | Examen={exam} | Total={final}")

            if past_grades:
                lines.append("\n[REGISTROS HISTÓRICOS - SEMESTRES PASADOS]")
                past_by_period = {}
                for g in past_grades:
                    if g.academic_period not in past_by_period:
                        past_by_period[g.academic_period] = []
                    past_by_period[g.academic_period].append(g)
                
                for period, p_grades in past_by_period.items():
                    lines.append(f" Periodo {period}:")
                    for g in p_grades:
                        lines.append(f"   - {g.subject.name}: Nota Final={g.final_grade}/200 ({g.get_status_display()})")
        else:
            lines.append("No se encontró historial académico.")

        lines.append("")

        # Horarios
        enrollments = Enrollment.objects.filter(
            student=student,
            academic_period=current_period,
            status='active'
        ).select_related('schedule__subject', 'schedule__professor', 'schedule__classroom')

        if enrollments.exists():
            lines.append(f"HORARIO DE CLASES (PERÍODO ACTUAL {current_period}):")
            for enrollment in enrollments:
                sched = enrollment.schedule
                # Calcular horas exactas de clase
                start = sched.start_time
                end = sched.end_time
                duracion_horas = (end.hour * 60 + end.minute - (start.hour * 60 + start.minute)) / 60.0
                
                lines.append(
                    f"  • Materia: {sched.subject.name}\n"
                    f"    Día: {sched.get_day_of_week_display()}\n"
                    f"    Hora: {start.strftime('%H:%M')} a {end.strftime('%H:%M')} (Duración: {duracion_horas} horas)\n"
                    f"    Profesor: {sched.professor.full_name}\n"
                    f"    Ubicación: Aula {sched.classroom.code} ({sched.classroom.get_building_display()}, Piso {sched.classroom.floor})"
                )
                
            from ..students.models import Activity, ActivitySubmission
            enrolled_subjects = [e.schedule.subject for e in enrollments]
            activities = Activity.objects.filter(subject__in=enrolled_subjects).order_by('due_date')
            
            if activities.exists():
                lines.append("\nACTIVIDADES Y TAREAS PENDIENTES:")
                for act in activities:
                    submission = ActivitySubmission.objects.filter(activity=act, student=student).first()
                    estado = "Entregado" if submission else "No entregado"
                    lines.append(f"  • {act.title} ({act.subject.name})")
                    lines.append(f"    Vence: {act.due_date.strftime('%Y-%m-%d %H:%M')}")
                    lines.append(f"    Estado: {estado}")
            else:
                lines.append("\nACTIVIDADES Y TAREAS PENDIENTES: Ninguna asignada.")

        return "\n".join(lines)

    def get_conversation_history(self, student: Optional[Student], session_id: str, limit: int = 5) -> list:
        """Obtiene el historial si hay estudiante, de lo contrario retorna vacío."""
        if not student:
            return []

        messages = ConversationHistory.objects.filter(
            student=student,
            session_id=session_id,
        ).order_by('-timestamp')[:limit * 2]

        history = []
        for msg in reversed(messages):
            history.append({
                "role": msg.role,
                "content": msg.message,
            })
        return history

    def save_message(self, student: Optional[Student], session_id: str, role: str,
                     message: str, context_used: dict = None, tokens_used: int = 0):
        """Solo guarda mensaje si hay estudiante (según requerimiento del usuario)."""
        if not student:
            return

        ConversationHistory.objects.create(
            student=student,
            session_id=session_id,
            role=role,
            message=message,
            context_used=context_used or {},
            tokens_used=tokens_used,
        )

    def generate_response(
        self,
        student: Optional[Student],
        user_message: str,
        session_id: str,
        request=None,
    ) -> dict:
        """
        Pipeline principal adaptado para acceso público (solo RAG) y privado (Student Context + RAG).
        """
        # 1. Historial de conversación (solo si hay estudiante) ANTES de guardar el nuevo mensaje
        conversation_history = self.get_conversation_history(student, session_id, limit=4)

        # 2. Guardar mensaje del usuario (solo si hay estudiante)
        self.save_message(student, session_id, 'user', user_message)

        # 3. Respuestas directas con herramientas internas/externas controladas
        direct_response = self._direct_tool_response(user_message)
        if direct_response:
            direct_response['session_id'] = str(session_id)
            context_used = {
                'tool_used': direct_response.get('tool_used'),
                'had_student_context': student is not None,
                'query_preview': user_message[:100],
            }
            self.save_message(
                student,
                session_id,
                'assistant',
                direct_response['response'],
                context_used,
                direct_response.get('tokens_used', 0),
            )
            if student:
                AuditLogService.log_chat_query(
                    user=student.user,
                    query=user_message,
                    response_preview=direct_response['response'][:100],
                    tokens_used=0,
                    request=request,
                )
            return direct_response

        # 4. Contexto operativo y académico
        system_context = self.get_system_context()
        student_context = self.get_student_context(student)

        # 5. Búsqueda RAG (siempre activa)
        rag_results = rag_engine.search(user_message)
        rag_context = rag_engine.format_context(rag_results)

        # 6. Construir mensajes
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "system", "content": system_context},
        ]
        
        if student_context:
            messages.append({
                "role": "system", 
                "content": f"CONTEXTO ACADÉMICO DEL ESTUDIANTE:\n{student_context}"
            })
            
        messages.append({
            "role": "system",
            "content": f"INFORMACIÓN DE DOCUMENTOS INSTITUCIONALES PUCESI:\n{rag_context}"
        })

        messages.extend(conversation_history)
        messages.append({"role": "user", "content": user_message})

        # 7. Llamar al LLM
        try:
            client = self.get_client()
            response = client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=messages,
                max_tokens=250,
                temperature=0.0,
            )

            assistant_message = response.choices[0].message.content
            tokens_used = response.usage.total_tokens

            # 7. Guardar respuesta (solo si hay estudiante)
            context_used = {
                'rag_sources': [r['source'] for r in rag_results],
                'rag_chunks_count': len(rag_results),
                'had_student_context': student is not None,
            }
            self.save_message(
                student, session_id, 'assistant',
                assistant_message, context_used, tokens_used
            )

            # 8. Registrar en audit log (solo si está autenticado)
            if student:
                AuditLogService.log_chat_query(
                    user=student.user,
                    query=user_message,
                    response_preview=assistant_message[:100],
                    tokens_used=tokens_used,
                    request=request,
                )

            return {
                'response': assistant_message,
                'tokens_used': tokens_used,
                'rag_sources': [r['source'] for r in rag_results],
                'session_id': str(session_id),
            }

        except Exception as e:
            logger.error(f"Error generando respuesta: {e}")
            error_msg = (
                "Lo siento, ocurrió un error al procesar tu consulta. "
                "Por favor intenta nuevamente."
            )
            self.save_message(student, session_id, 'assistant', error_msg)
            return {
                'response': error_msg,
                'tokens_used': 0,
                'rag_sources': [],
                'session_id': str(session_id),
                'error': str(e),
            }


# Instancia singleton del servicio
chatbot_service = ChatbotService()
