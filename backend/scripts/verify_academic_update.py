import os
import django
import uuid

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.students.models import Student, Grade, Subject, Notification
from django.contrib.auth import get_user_model

User = get_user_model()

def test_academic_update():
    # 1. Obtener o crear estudiante de prueba
    user = User.objects.filter(username='EST-001').first()
    if not user:
        user = User.objects.create_user(username='EST-001', password='password123', first_name='Estudiante', last_name='Prueba')
    
    student, _ = Student.objects.get_or_create(
        user=user,
        defaults={'student_code': 'EST-001', 'career_start_date': '2024-01-01'}
    )

    # 2. Crear materia
    subject, _ = Subject.objects.get_or_create(
        code='PROG1',
        defaults={'name': 'Programación I', 'semester': 1, 'carrera': 'IDS'}
    )

    # 3. Crear nota (P1=35, P2=40, P3=25 -> Debería ser Reprobado por P3 < 30)
    grade, _ = Grade.objects.update_or_create(
        student=student,
        subject=subject,
        academic_period='2024-2025-II',
        defaults={
            'partial_1': 35,
            'partial_2': 40,
            'partial_3': 40,
            'final_exam': 40
        }
    )
    # Total = 155. Todas > 30.
    grade.save() # Dispara calculate_final
    print(f"Materia: {grade.subject.name} | Total: {grade.final_grade} | Estado: {grade.status}")

    # 4. Crear notificación
    Notification.objects.create(
        student=student,
        title="Nueva Nota Publicada",
        message="Se ha registrado tu nota del Examen Final de Programación I."
    )
    print("Notificación de prueba creada.")

if __name__ == "__main__":
    test_academic_update()
