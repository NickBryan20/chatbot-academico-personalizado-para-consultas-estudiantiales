import os
import sys
import django
import random
from pathlib import Path

# Setup Django
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.students.models import Student, Grade, Enrollment, Subject

def update_grades():
    print("Iniciando actualizacion masiva de notas a escala 50 (Total 200)...")
    
    students = Student.objects.all()
    if not students.exists():
        print("❌ No se encontraron estudiantes.")
        return

    # Asegurarnos de que existan materias para asignar
    subjects = Subject.objects.all()
    if not subjects.exists():
        print("❌ No se encontraron materias.")
        return

    period = '2024-2025-II'
    count = 0

    for student in students:
        # Por cada estudiante, busquemos o creemos un par de inscripciones
        # Si no tiene inscripciones, creamos una para mostrar datos
        enrollments = Enrollment.objects.filter(student=student, academic_period=period)
        
        if not enrollments.exists():
            # Inscribir en una materia aleatoria si no tiene nada
            sub = random.choice(subjects)
            # Intentar buscar un schedule para esa materia (simplificado)
            from apps.students.models import Schedule
            sched = Schedule.objects.filter(subject=sub).first()
            if sched:
                Enrollment.objects.create(student=student, schedule=sched, academic_period=period)
                enrollments = Enrollment.objects.filter(student=student, academic_period=period)

        for enrollment in enrollments:
            # Crear o actualizar Grade
            grade, created = Grade.objects.get_or_create(
                student=student,
                subject=enrollment.schedule.subject,
                academic_period=period
            )
            
            # Generar notas variadas según solicitud del usuario
            # Rango promedio: 35-48
            # Rango bajo: 20-29
            # Probabilidad: 80% promedio, 20% bajo
            
            def get_varied_grade():
                if random.random() > 0.2:
                    return random.randint(35, 50) # Promedio/Alto
                else:
                    return random.randint(20, 31) # Bajo/Reprobando

            grade.partial_1 = get_varied_grade()
            grade.partial_2 = get_varied_grade()
            grade.partial_3 = get_varied_grade()
            grade.final_exam = get_varied_grade()
            
            # La suma se calcula automáticamente en el save() del modelo
            grade.save()
            count += 1
            
    print(f"✅ Se actualizaron {count} registros de calificaciones.")

if __name__ == "__main__":
    update_grades()
