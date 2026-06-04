"""
Modelos académicos: Student, Subject, Professor, Classroom,
Schedule, Enrollment, Grade, ConversationHistory.
"""
import uuid
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Student(models.Model):
    """Perfil académico del estudiante vinculado al usuario del sistema."""

    CARRERA_CHOICES = [
        ('IDS', 'Ingeniería en Desarrollo de Software'),
        ('ITI', 'Ingeniería en Tecnologías de la Información'),
        ('ADM', 'Administración de Empresas'),
        ('AGR', 'Agronomía'),
        ('ZOO', 'Zootecnia'),
        ('VET', 'Medicina Veterinaria'),
        ('ENF', 'Enfermería'),
        ('DER', 'Derecho'),
        ('ARQ', 'Arquitectura'),
        ('NEG', 'Negocios Internacionales'),
        ('GAS', 'Gastronomía'),
        ('DIS', 'Diseño Gráfico'),
        ('AUD', 'Auditoría y Gestión Contable'),
        ('CIV', 'Ingeniería Civil'),
        ('IAM', 'Ingeniería Ambiental'),
        ('PED', 'Pedagogía de los Idiomas'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )
    student_code = models.CharField(max_length=20, unique=True, help_text="ej: EST-001")
    carrera = models.CharField(max_length=3, choices=CARRERA_CHOICES, default='IDS')
    semester_current = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    career_start_date = models.DateField()
    photo = models.ImageField(upload_to='student_photos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'student'
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'
        ordering = ['student_code']

    def __str__(self):
        return f"{self.student_code} — {self.user.get_full_name()} ({self.get_carrera_display()})"

    @property
    def full_name(self):
        return self.user.get_full_name()

    @property
    def email(self):
        return self.user.email


class Professor(models.Model):
    """Docente de la PUCESI."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='professor_profile'
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    specialization = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'professor'
        verbose_name = 'Docente'
        verbose_name_plural = 'Docentes'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"Dr./Ing. {self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Classroom(models.Model):
    """Aula o laboratorio de la PUCESI."""

    BUILDING_CHOICES = [
        ('A', 'Edificio A'),
        ('B', 'Edificio B'),
        ('C', 'Edificio C'),
        ('LAB', 'Laboratorios'),
        ('AUD', 'Auditorio'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10, unique=True, help_text="ej: A-101")
    building = models.CharField(max_length=3, choices=BUILDING_CHOICES)
    floor = models.PositiveSmallIntegerField(default=1)
    capacity = models.PositiveSmallIntegerField(default=30)
    is_lab = models.BooleanField(default=False)

    class Meta:
        db_table = 'classroom'
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'
        ordering = ['code']

    def __str__(self):
        tipo = "Laboratorio" if self.is_lab else "Aula"
        return f"{tipo} {self.code} — {self.get_building_display()} ({self.capacity} estudiantes)"


class Subject(models.Model):
    """Materia del pensum académico."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=200)
    credits = models.PositiveSmallIntegerField(default=4)
    semester = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    carrera = models.CharField(max_length=3, choices=Student.CARRERA_CHOICES, default='IDS')
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'subject'
        verbose_name = 'Materia'
        verbose_name_plural = 'Materias'
        ordering = ['carrera', 'semester', 'name']

    def __str__(self):
        return f"[{self.code}] {self.name} — Semestre {self.semester}"


class Schedule(models.Model):
    """Horario de clase: materia + profesor + aula + día + hora."""

    DAY_CHOICES = [
        ('MON', 'Lunes'),
        ('TUE', 'Martes'),
        ('WED', 'Miércoles'),
        ('THU', 'Jueves'),
        ('FRI', 'Viernes'),
        ('SAT', 'Sábado'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='schedules')
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='schedules')
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='schedules')
    day_of_week = models.CharField(max_length=3, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    academic_period = models.CharField(max_length=20, help_text="ej: 2024-2025-II")

    class Meta:
        db_table = 'schedule'
        verbose_name = 'Horario'
        verbose_name_plural = 'Horarios'
        ordering = ['day_of_week', 'start_time']

    def __str__(self):
        return (f"{self.subject.name} — {self.get_day_of_week_display()} "
                f"{self.start_time}-{self.end_time} | Aula {self.classroom.code}")


class Enrollment(models.Model):
    """Matrícula: relación estudiante ↔ horario."""

    STATUS_CHOICES = [
        ('active', 'Activo'),
        ('withdrawn', 'Retirado'),
        ('completed', 'Completado'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='enrollments')
    academic_period = models.CharField(max_length=20)
    enrollment_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    class Meta:
        db_table = 'enrollment'
        verbose_name = 'Matrícula'
        verbose_name_plural = 'Matrículas'
        unique_together = ['student', 'schedule', 'academic_period']

    def __str__(self):
        return f"{self.student.student_code} → {self.schedule.subject.name} ({self.academic_period})"


class Grade(models.Model):
    """Notas del estudiante por materia y período académico."""

    STATUS_CHOICES = [
        ('approved', 'Aprobado'),
        ('failed', 'Reprobado'),
        ('pending', 'En curso'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='grades')
    academic_period = models.CharField(max_length=20)

    # Notas (escala 0.00 - 50.00)
    partial_1 = models.DecimalField(
        max_digits=5, decimal_places=2,
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(50)]
    )
    partial_2 = models.DecimalField(
        max_digits=5, decimal_places=2,
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(50)]
    )
    partial_3 = models.DecimalField(
        max_digits=5, decimal_places=2,
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(50)]
    )
    final_exam = models.DecimalField(
        max_digits=5, decimal_places=2,
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(50)]
    )
    final_grade = models.DecimalField(
        max_digits=6, decimal_places=2,
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(200)]
    )
    attendance_percentage = models.DecimalField(
        max_digits=5, decimal_places=2,
        default=0.0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Porcentaje de asistencia (mínimo 80% para aprobar)"
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    class Meta:
        db_table = 'grade'
        verbose_name = 'Nota'
        verbose_name_plural = 'Notas'
        unique_together = ['student', 'subject', 'academic_period']
        indexes = [
            models.Index(fields=['student', 'academic_period']),
        ]

    def __str__(self):
        return (f"{self.student.student_code} — {self.subject.name} "
                f"({self.academic_period}): {self.final_grade or 'En curso'}")

    def calculate_final(self):
        """Calcula el acumulado y verifica aprobación (30/50 min por fase, 120 total)."""
        components = [self.partial_1, self.partial_2, self.partial_3, self.final_exam]
        
        # Solo calculamos si todas las notas están presentes
        if all(c is not None for c in components):
            total = sum(components)
            self.final_grade = total
            
            # Requisito: Mínimo 30 en cada fase y 120 en total
            passed_phases = all(float(c) >= 30.0 for c in components)
            if total >= 120 and passed_phases:
                self.status = 'approved'
            else:
                self.status = 'failed'
        else:
            self.status = 'pending'
            self.final_grade = sum(c for c in components if c is not None)
            
        return self.final_grade

    def save(self, *args, **kwargs):
        self.calculate_final()
        super().save(*args, **kwargs)


class Notification(models.Model):
    """Sistema de notificaciones para estudiantes."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notification'
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student.student_code}: {self.title}"


class ConversationHistory(models.Model):
    """Historial de conversaciones del chatbot por estudiante."""

    ROLE_CHOICES = [
        ('user', 'Usuario'),
        ('assistant', 'Asistente'),
        ('system', 'Sistema'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='conversations')
    session_id = models.UUIDField(default=uuid.uuid4, db_index=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    message = models.TextField()
    context_used = models.JSONField(
        default=dict, blank=True,
        help_text="Fragmentos RAG y datos DB usados para esta respuesta"
    )
    tokens_used = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'conversation_history'
        verbose_name = 'Historial de Conversación'
        verbose_name_plural = 'Historiales de Conversación'
        ordering = ['session_id', 'timestamp']
        indexes = [
            models.Index(fields=['student', 'session_id']),
            models.Index(fields=['student', 'timestamp']),
        ]

    def __str__(self):
        preview = self.message[:50] + '...' if len(self.message) > 50 else self.message
        return f"[{self.role}] {self.student.student_code}: {preview}"


class Activity(models.Model):
    """Actividad o Tarea asignada por el profesor en una materia."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='activities')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField()
    file = models.FileField(upload_to='activities/instructions/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'activity'
        verbose_name = 'Actividad'
        verbose_name_plural = 'Actividades'
        ordering = ['due_date']
        
    def __str__(self):
        return f"{self.title} - {self.subject.name} (Vence: {self.due_date.strftime('%Y-%m-%d')})"


class ActivitySubmission(models.Model):
    """Entrega de la actividad por parte del estudiante."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='submissions')
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='submissions')
    file = models.FileField(upload_to='activities/submissions/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    comments = models.TextField(blank=True)
    grade = models.DecimalField(
        max_digits=5, decimal_places=2,
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(50)]
    )
    
    class Meta:
        db_table = 'activity_submission'
        verbose_name = 'Entrega'
        verbose_name_plural = 'Entregas'
        unique_together = ['student', 'activity']
        
    def __str__(self):
        return f"Entrega de {self.student.student_code} para {self.activity.title}"
