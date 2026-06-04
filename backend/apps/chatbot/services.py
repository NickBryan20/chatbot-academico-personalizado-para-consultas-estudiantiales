"""
Servicio del Chatbot: pipeline completo de generación de respuestas.
Integra: datos académicos del estudiante + RAG + OpenAI LLM.
El sistema NO genera información inventada.
"""
import logging
from typing import Optional

from django.conf import settings
from django.utils import timezone

from ..students.models import Student, Grade, Schedule, Enrollment, ConversationHistory
from ..rag.engine import rag_engine
from ..audit_logs.services import AuditLogService

logger = logging.getLogger(__name__)

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
10. CAMPUS Y CALIFICACIONES: Para ubicación de aulas, edificios, biblioteca, bar/cafetería, copias, tesorería, secretaría y carnet institucional, consulta primero el mapa de campus validado. Para calificaciones, usa la regla del prototipo: 4 componentes de 50 puntos, mínimo 30/50 por componente, 120/200 total y 80% de asistencia.
11. HORARIOS Y PRERREQUISITOS: Si el estudiante autenticado pregunta por "mi horario", usa su contexto académico de base de datos. Si pregunta por horarios oficiales, prerrequisitos, NRC o PDFs por carrera del periodo 2026-01, usa la página oficial de Horarios Estudiantiles 2026-01 y no inventes prerrequisitos específicos.
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

        # 0. Agregar Fecha y Hora Actual para resolver preguntas relativas (hoy, mañana)
        import locale
        try:
            locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        except:
            pass
        now = timezone.localtime(timezone.now())
        lines.insert(0, f"FECHA Y HORA ACTUAL DEL SISTEMA: {now.strftime('%A, %d de %B de %Y - %H:%M')}\n(Usa esta fecha para determinar qué clases tiene 'hoy' o 'mañana')\n")

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

        # 3. Contexto académico (estudiante o vacío)
        student_context = self.get_student_context(student)

        # 4. Búsqueda RAG (siempre activa)
        rag_results = rag_engine.search(user_message)
        rag_context = rag_engine.format_context(rag_results)

        # 5. Construir mensajes
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
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

        # 6. Llamar al LLM
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
