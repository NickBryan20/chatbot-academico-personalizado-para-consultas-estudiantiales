import os
import sys
import django
import random
from datetime import time
from pathlib import Path

# Setup Django
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.students.models import Student, Subject, Professor, Classroom, Schedule, Enrollment, Grade
from django.contrib.auth import get_user_model

User = get_user_model()

# MALLA CURRICULAR: INGENIERÍA EN TECNOLOGÍAS DE LA INFORMACIÓN (6 materias x 10 niveles)
IT_CURRICULUM = {
    1: [
        ("IT-101", "Fundamentos de Programación"), ("IT-102", "Álgebra Lineal"), 
        ("IT-103", "Introducción a las TIC"), ("IT-104", "Comunicación Oral y Escrita"),
        ("IT-105", "Realidad Socioeconómica"), ("IT-106", "Ética y Pensamiento Cristiano")
    ],
    2: [
        ("IT-201", "Estructuras de Datos"), ("IT-202", "Cálculo Diferencial"), 
        ("IT-203", "Arquitectura de Computadores"), ("IT-204", "Sistemas Operativos"),
        ("IT-205", "Matemática Discreta"), ("IT-206", "Ciudadanía y Servicio")
    ],
    3: [
        ("IT-301", "Programación Orientada a Objetos"), ("IT-302", "Cálculo Integral"), 
        ("IT-303", "Redes de Datos I"), ("IT-304", "Base de Datos I"),
        ("IT-305", "Física para IT"), ("IT-306", "Pensamiento Sistémico")
    ],
    4: [
        ("IT-401", "Desarrollo de Aplicaciones Web"), ("IT-402", "Probabilidad y Estadística"), 
        ("IT-403", "Redes de Datos II"), ("IT-404", "Base de Datos II"),
        ("IT-405", "Metodologías Ágiles"), ("IT-406", "Programación de Bajo Nivel")
    ],
    5: [
        ("IT-501", "Desarrollo de Aplicaciones Móviles"), ("IT-502", "Investigación de Operaciones"), 
        ("IT-503", "Ciberseguridad I"), ("IT-504", "Ingeniería de Software"),
        ("IT-505", "Programación en la Nube"), ("IT-506", "Proyecto Integrador I")
    ],
    6: [
        ("IT-601", "Inteligencia Artificial"), ("IT-602", "Minería de Datos"), 
        ("IT-603", "Ciberseguridad II"), ("IT-604", "Gestión de Proyectos TI"),
        ("IT-605", "Servicios IP y Telefonía"), ("IT-606", "Proyecto Integrador II")
    ],
    7: [
        ("IT-701", "Machine Learning"), ("IT-702", "Análisis de Datos Avanzado"), 
        ("IT-703", "Auditoría de Sistemas"), ("IT-704", "Gobernanza de TI"),
        ("IT-705", "Sistemas Distribuidos"), ("IT-706", "Emprendimiento TIC")
    ],
    8: [
        ("IT-801", "Gestión de Servicios TI (ITIL)"), ("IT-802", "Cloud Computing Avanzado"), 
        ("IT-803", "Ética Profesional IT"), ("IT-804", "Infraestructura Crítica"),
        ("IT-805", "Prácticas Pre-profesionales I"), ("IT-806", "Proyecto Integrador III")
    ],
    9: [
        ("IT-901", "Deep Learning"), ("IT-902", "Big Data"), 
        ("IT-903", "Seguridad de la Información"), ("IT-904", "Gerencia de TI"),
        ("IT-905", "Prácticas II"), ("IT-906", "Trabajo de Titulación I")
    ],
    10: [
        ("IT-1001", "Internet de las Cosas (IoT)"), ("IT-1002", "Blockchain"), 
        ("IT-1003", "Gestión de Riesgos TI"), ("IT-1004", "Simulacros de Certificación"),
        ("IT-1005", "Prácticas III"), ("IT-1006", "Trabajo de Titulación II")
    ]
}

PROFESSORS = [
    ("Augusto", "Cueva"), ("Tania", "López"), ("Mario", "Ponce"), ("Andrés", "Vaca"),
    ("Lucía", "Figueroa"), ("Roberto", "Benavides"), ("Ximena", "García"), ("Paúl", "Salazar")
]

CLASSROOMS = [
    ("A-101", "A"), ("A-202", "A"), ("B-105", "B"), ("C-301", "C"), ("LAB-1", "LAB"), ("LAB-2", "LAB")
]

PERIODS = ["2022-I", "2022-II", "2023-I", "2023-II", "2024-I", "2024-2025-II"]

def populate():
    print("--- INICIANDO RECONSTRUCCION DEL UNIVERSO ACADEMICO (IT) ---")
    
    # 1. Limpiar datos antiguos (excepto Usuarios)
    print("Limpiando datos antiguos...")
    Grade.objects.all().delete()
    Enrollment.objects.all().delete()
    Schedule.objects.all().delete()
    Subject.objects.all().delete()
    Professor.objects.all().delete()
    Classroom.objects.all().delete()

    # 2. Crear Profesores y Aulas
    prof_objs = []
    for f, l in PROFESSORS:
        p = Professor.objects.create(first_name=f, last_name=l, email=f"{f.lower()}.{l.lower()}@pucesi.edu.ec")
        prof_objs.append(p)

    room_objs = []
    for c, b in CLASSROOMS:
        r = Classroom.objects.create(code=c, building=b, floor=1 if "1" in c else 2)
        room_objs.append(r)

    # 3. Crear Materias (Malla IT) y Horarios
    print("Creando 60 materias de la malla IT...")
    subject_map = {} # level -> list of subjects
    for level, subjects in IT_CURRICULUM.items():
        subject_map[level] = []
        for code, name in subjects:
            s = Subject.objects.create(code=code, name=name, semester=level, carrera='IDS') # Usamos IDS como alias de TI en el modelo
            subject_map[level].append(s)
            
            # Crear Horario para cada materia
            day = random.choice(['MON', 'TUE', 'WED', 'THU', 'FRI'])
            start = time(random.randint(7, 18), 0)
            end = time(start.hour + 2, 0)
            Schedule.objects.create(
                subject=s, professor=random.choice(prof_objs), classroom=random.choice(room_objs),
                day_of_week=day, start_time=start, end_time=end, academic_period="2024-2025-II"
            )

    # 4. Procesar Estudiantes
    students = Student.objects.all()
    print(f"Sincronizando historial para {students.count()} estudiantes...")
    
    for student in students:
        N = student.semester_current
        # Generar historial para cada semestre anterior (1 a N-1)
        for level in range(1, N):
            period = PERIODS[level % len(PERIODS)]
            subjects = subject_map[level]
            for s in subjects:
                # Grade histórica
                p1, p2, p3, final_ex = [random.randint(30, 50) for _ in range(4)]
                attendance = random.randint(85, 100)
                Grade.objects.create(
                    student=student, subject=s, academic_period=period,
                    partial_1=p1, partial_2=p2, partial_3=p3, final_exam=final_ex,
                    final_grade=p1+p2+p3+final_ex, attendance_percentage=attendance,
                    status='approved'
                )

        # Generar semestre actual (N)
        current_period = "2024-2025-II"
        current_subjects = subject_map[N]
        for s in current_subjects:
            # Enrollment
            sched = s.schedules.filter(academic_period=current_period).first()
            if sched:
                Enrollment.objects.create(student=student, schedule=sched, academic_period=current_period)
            
            # Grade "En curso"
            # Solo notas parciales iniciales (o aleatorias para demo)
            p1 = random.randint(30, 50)
            p2 = random.randint(25, 45)
            attendance = random.randint(75, 95)
            Grade.objects.create(
                student=student, subject=s, academic_period=current_period,
                partial_1=p1, partial_2=p2, attendance_percentage=attendance,
                status='pending'
            )

    print("Universo academico IT reconstruido exitosamente.")

if __name__ == "__main__":
    populate()
