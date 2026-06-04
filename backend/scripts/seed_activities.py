import os
import sys
import django
from datetime import timedelta
from django.utils import timezone

# Setup Django environment
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from apps.students.models import Student, Activity, Enrollment

def seed_activities():
    print("Iniciando creación de actividades de prueba...")
    
    # 1. Obtener al estudiante de prueba (nlopezr)
    try:
        user = django.contrib.auth.models.User.objects.get(username='nlopezr')
        student = Student.objects.get(user=user)
    except Exception as e:
        print(f"Estudiante de prueba nlopezr no encontrado. Crearemos actividades para todos. Error: {e}")
        student = None
        
    # Buscar materias en las que está matriculado
    if student:
        enrolled_subjects = Enrollment.objects.filter(student=student, status='active').values_list('schedule__subject', flat=True)
        from apps.students.models import Subject
        subjects = Subject.objects.filter(id__in=enrolled_subjects)
    else:
        from apps.students.models import Subject
        subjects = Subject.objects.all()[:3]
        
    if not subjects.exists():
        print("No se encontraron materias matriculadas para crear actividades.")
        return
        
    now = timezone.now()
    created_count = 0
    
    for idx, subject in enumerate(subjects):
        # Crear una actividad que venza en un par de días
        Activity.objects.get_or_create(
            subject=subject,
            title=f"Taller Nro 9_{idx+1}: Herramientas de {subject.name[:10]}...",
            defaults={
                'description': f"Este es un deber de prueba para la materia {subject.name}.",
                'due_date': now + timedelta(days=3, hours=5),
            }
        )
        created_count += 1
        
        # Otra actividad que venza pronto
        Activity.objects.get_or_create(
            subject=subject,
            title=f"Investigación Formativa: {subject.name}",
            defaults={
                'description': f"Debe subir el PDF con la investigación.",
                'due_date': now + timedelta(hours=12),
            }
        )
        created_count += 1

    print(f"✅ ¡Se crearon {created_count} actividades de prueba con éxito!")

if __name__ == '__main__':
    seed_activities()
