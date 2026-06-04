"""Controladores de negocio para el módulo de Estudiantes."""
from django.db.models import Avg, Sum
from ..audit_logs.services import AuditLogService
from .models import Student, Grade, Enrollment, Notification

class EstudianteControlador:
    """
    Controlador principal para la lógica de negocio de Estudiantes.
    Todos sus métodos son estáticos y reciben request para auditoría.
    Evita la manipulación directa de modelos en las vistas.
    """
    @staticmethod
    def obtener_perfil(user, request):
        """
        Obtiene el perfil del estudiante autenticado.
        Registra el acceso en AuditLog.
        """
        student = Student.objects.get(user=user)
        AuditLogService.log_data_access(user, 'profile', request)
        return student

    @staticmethod
    def obtener_calificaciones(user, period, request):
        """
        Consulta las calificaciones del estudiante.
        Permite filtrar por periodo académico específico (ej: 2026-01).
        """
        student = Student.objects.get(user=user)
        grades = Grade.objects.filter(student=student).select_related('subject')
        if period:
            grades = grades.filter(academic_period=period)
        grades = grades.order_by('-academic_period', 'subject__semester')
        
        AuditLogService.log_data_access(user, 'grades_history', request)
        return grades

    @staticmethod
    def obtener_horario(user, period, request):
        """
        Extrae los horarios de las clases a las que el estudiante está inscrito.
        Retorna la relación con materia, profesor y aula.
        """
        student = Student.objects.get(user=user)
        enrollments = Enrollment.objects.filter(
            student=student, 
            academic_period=period,
            status='active'
        ).select_related('schedule__subject', 'schedule__professor', 'schedule__classroom')
        
        AuditLogService.log_data_access(user, 'schedule', request)
        return [e.schedule for e in enrollments]

    @staticmethod
    def obtener_estadisticas(user):
        """
        Calcula el GPA, créditos totales y porcentaje de asistencia.
        Útil para mostrar el resumen en el Dashboard del estudiante.
        """
        student = Student.objects.get(user=user)
        current_period = '2026-01'
        
        all_grades = Grade.objects.filter(student=student, status='approved')
        gpa = all_grades.aggregate(Avg('final_grade'))['final_grade__avg'] or 0.0
        passed_count = all_grades.count()
        
        current_grades = Grade.objects.filter(student=student, academic_period=current_period)
        avg_attendance = current_grades.aggregate(Avg('attendance_percentage'))['attendance_percentage__avg'] or 0.0
        
        total_credits = all_grades.aggregate(Sum('subject__credits'))['subject__credits__sum'] or 0
        
        return {
            'gpa': round(float(gpa), 2),
            'passed_subjects': passed_count,
            'attendance_avg': round(float(avg_attendance), 1),
            'total_credits': total_credits,
            'current_semester': student.semester_current
        }

    @staticmethod
    def obtener_notificaciones(user, unread_only=False):
        """
        Devuelve el buzón de notificaciones del estudiante.
        Si unread_only es True, filtra solo las no leídas.
        """
        student = Student.objects.get(user=user)
        notifications = Notification.objects.filter(student=student)
        if unread_only:
            notifications = notifications.filter(is_read=False)
        return notifications

    @staticmethod
    def marcar_notificacion_leida(user, pk):
        """
        Marca una notificación específica como leída en la base de datos.
        """
        student = Student.objects.get(user=user)
        notification = Notification.objects.get(pk=pk, student=student)
        notification.is_read = True
        notification.save()
        return True

    @staticmethod
    def obtener_actividades(user, request):
        """
        Busca las materias en las que está inscrito y obtiene los deberes o 
        actividades pendientes de esas materias.
        """
        student = Student.objects.get(user=user)
        enrolled_subjects = Enrollment.objects.filter(student=student, status='active').values_list('schedule__subject', flat=True)
        from .models import Activity
        activities = Activity.objects.filter(subject__in=enrolled_subjects).order_by('due_date')
        AuditLogService.log_data_access(user, 'activities', request)
        return activities

    @staticmethod
    def entregar_actividad(user, activity_id, file, comments, request):
        """
        Sube o actualiza la entrega (archivo y comentarios) de un deber.
        Registra la acción para auditoría.
        """
        student = Student.objects.get(user=user)
        from .models import Activity, ActivitySubmission
        activity = Activity.objects.get(id=activity_id)
        
        submission, created = ActivitySubmission.objects.get_or_create(
            student=student, 
            activity=activity,
            defaults={'file': file, 'comments': comments}
        )
        if not created:
            if file:
                submission.file = file
            if comments:
                submission.comments = comments
            submission.save()
            
        AuditLogService.log_data_access(user, 'submit_activity', request)
        return submission
