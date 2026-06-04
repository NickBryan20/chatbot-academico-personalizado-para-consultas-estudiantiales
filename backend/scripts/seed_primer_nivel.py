"""
Script para poblar la base de datos con 100 estudiantes simulados,
todos de primer nivel, en carreras específicas:
- Ingeniería Civil (CIV)
- Ingeniería en Desarrollo de Software (IDS)
- Ingeniería Ambiental (IAM)
- Agronomía (AGR)
- Ingeniería en Tecnologías de la Información (ITI)

Uso:
    python manage.py runscript seed_primer_nivel
    -- o --
    python scripts/seed_primer_nivel.py
"""
import os
import sys
import django
import random
import secrets
from datetime import date, time
from decimal import Decimal

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.contrib.auth.hashers import make_password
from django.conf import settings
from apps.authentication.models import User
from apps.students.models import (
    Student, Professor, Classroom, Subject, Schedule, Enrollment, Grade
)

DEFAULT_STUDENT_PASSWORD = settings.SEED_STUDENT_PASSWORD or secrets.token_urlsafe(12)
DEFAULT_TEACHER_PASSWORD = settings.SEED_TEACHER_PASSWORD or secrets.token_urlsafe(12)

# ─── DATOS BASE ─────────────────────────────────────────────────────────────

CARRERAS = ['CIV', 'IDS', 'IAM', 'AGR', 'ITI']

NOMBRES = [
    'Santiago', 'Valentina', 'Andrés', 'Camila', 'Diego', 'Isabella', 'Mateo',
    'Sofía', 'Sebastián', 'Lucía', 'Nicolás', 'Valeria', 'Emilio', 'Daniela',
    'Gabriel', 'Paula', 'Alejandro', 'Andrea', 'Fernando', 'María', 'David',
    'Carolina', 'Carlos', 'Ana', 'Pablo', 'Natalia', 'Jorge', 'Paola',
    'Roberto', 'Gabriela', 'Felipe', 'Diana', 'Iván', 'Melissa', 'Cristian',
    'Laura', 'Luis', 'Karina', 'Miguel', 'Verónica',
]

APELLIDOS = [
    'García', 'Rodríguez', 'López', 'Martínez', 'González', 'Hernández',
    'Pérez', 'Sánchez', 'Ramírez', 'Torres', 'Flores', 'Rivera', 'Gómez',
    'Díaz', 'Morales', 'Muñoz', 'Álvarez', 'Ruiz', 'Jiménez', 'Vargas',
    'Suárez', 'Romero', 'Ortiz', 'Chávez', 'Reyes', 'Herrera', 'Mendoza',
    'Castro', 'Guerrero', 'Cruz', 'Vega', 'Ramos', 'Delgado', 'Ríos',
    'Mora', 'Salazar', 'Cárdenas', 'Cabrera', 'Espinoza', 'Molina',
]

PROFESORES_DATA = [
    ('María', 'Andrade', 'mandrade@pucesi.edu.ec', 'Matemáticas y Álgebra'),
    ('Carlos', 'Benavides', 'cbenavides@pucesi.edu.ec', 'Programación y Algoritmos'),
    ('Ana', 'Cisneros', 'acisneros@pucesi.edu.ec', 'Bases de Datos'),
    ('Jorge', 'Dávila', 'jdavila@pucesi.edu.ec', 'Redes y Comunicaciones'),
    ('Roberto', 'Espinoza', 'respinoza@pucesi.edu.ec', 'Ingeniería de Software'),
    ('Lucía', 'Flores', 'lflores@pucesi.edu.ec', 'Inteligencia Artificial'),
    ('Fabricio', 'Guerrero', 'fguerrero@pucesi.edu.ec', 'Sistemas Operativos'),
    ('Patricia', 'Herrera', 'pherrera@pucesi.edu.ec', 'Cálculo y Estadística'),
    ('Marcos', 'Imbaquingo', 'mimbaquingo@pucesi.edu.ec', 'Arquitectura de Software'),
    ('Verónica', 'Játiva', 'vjativa@pucesi.edu.ec', 'Desarrollo Web'),
    ('Eduardo', 'Paredes', 'eparedes@pucesi.edu.ec', 'Física y Mecánica'),
    ('Silvia', 'Maldonado', 'smaldonado@pucesi.edu.ec', 'Química y Biología'),
]

# Materias Primer Nivel (Mallas)
MATERIAS_DATA = [
    # Ingeniería Civil (CIV)
    ('CIV-101', 'Mecánica Racional', 4, 1, 'CIV'),
    ('CIV-102', 'Análisis Matemático I', 4, 1, 'CIV'),
    ('CIV-103', 'Álgebra Lineal', 4, 1, 'CIV'),
    ('CIV-104', 'Ciencia de los Materiales', 3, 1, 'CIV'),
    ('CIV-105', 'Tecnologías de la Información y de la Comunicación (TIC)', 3, 1, 'CIV'),
    ('CIV-106', 'Comunicación Oral y Escrita', 2, 1, 'CIV'),
    
    # Ingeniería en Desarrollo de Software (IDS)
    ('IDS-101', 'Comunicación Oral y Escrita', 2, 1, 'IDS'),
    ('IDS-102', 'Herramientas Digitales Aplicadas', 2, 1, 'IDS'),
    ('IDS-103', 'Habilidades Lógico Matemáticas', 3, 1, 'IDS'),
    ('IDS-104', 'Fundamentos de Programación', 4, 1, 'IDS'),
    ('IDS-105', 'Introducción al Desarrollo Web', 4, 1, 'IDS'),
    ('IDS-106', 'Algebra', 4, 1, 'IDS'),
    ('IDS-107', 'Sistemas Operativos', 3, 1, 'IDS'),
    ('IDS-108', 'Segunda Lengua A1', 2, 1, 'IDS'),

    # Ingeniería Ambiental (IAM)
    ('IAM-101', 'MATEMÁTICA I', 6, 1, 'IAM'),
    ('IAM-102', 'FÍSICA I', 4, 1, 'IAM'),
    ('IAM-103', 'QUÍMICA I', 4, 1, 'IAM'),
    ('IAM-104', 'REDACCIÓN TÉCNICA', 1, 1, 'IAM'),
    ('IAM-105', 'ÉTICA DE LA INGENIERÍA', 1, 1, 'IAM'),
    ('IAM-106', 'GEOLOGÍA GENERAL', 4, 1, 'IAM'),
    ('IAM-107', 'DIBUJO', 2, 1, 'IAM'),

    # Agronomía (AGR)
    ('AGR-101', 'Biología General', 4, 1, 'AGR'),
    ('AGR-102', 'Química General e Inorgánica', 4, 1, 'AGR'),
    ('AGR-103', 'Botánica Sistemática', 4, 1, 'AGR'),
    ('AGR-104', 'Matemáticas I', 4, 1, 'AGR'),
    ('AGR-105', 'Introducción a las Ciencias Agrícolas', 2, 1, 'AGR'),
    ('AGR-106', 'Lenguaje y Comunicación', 2, 1, 'AGR'),

    # Ingeniería en Tecnologías de la Información (ITI)
    ('ITI-101', 'Fundamentos de Tecnologías de la Información', 4, 1, 'ITI'),
    ('ITI-102', 'Lógica de Programación', 4, 1, 'ITI'),
    ('ITI-103', 'Matemáticas Discretas', 4, 1, 'ITI'),
    ('ITI-104', 'Arquitectura de Computadoras', 3, 1, 'ITI'),
    ('ITI-105', 'Comunicación Oral y Escrita', 2, 1, 'ITI'),
    ('ITI-106', 'Inglés I', 2, 1, 'ITI'),
]

AULAS_DATA = [
    ('A-101', 'A', 1, 35, False),
    ('A-102', 'A', 1, 35, False),
    ('B-101', 'B', 1, 30, False),
    ('LAB-01', 'LAB', 1, 25, True),
    ('LAB-02', 'LAB', 1, 25, True),
    ('LAB-03', 'LAB', 2, 20, True),
]

DIAS = ['MON', 'TUE', 'WED', 'THU', 'FRI']
HORARIOS_INICIO = [time(7, 0), time(9, 0), time(11, 0), time(14, 0), time(16, 0)]
PERIODO_ACTUAL = '2026-01'

def run():
    print("Iniciando limplieza y re-seed de base de datos...")
    print("=" * 60)

    # 0. Limpiar Datos Anteriores
    print("Limpiando datos actuales (Grades, Enrollments, Schedules, Students, Users)...")
    Grade.objects.all().delete()
    Enrollment.objects.all().delete()
    Schedule.objects.all().delete()
    Student.objects.all().delete()
    User.objects.filter(is_superuser=False).delete()
    Subject.objects.all().delete()

    # 1. CREAR PROFESORES
    print("\nCreando profesores...")
    profesores = []
    for first, last, email, spec in PROFESORES_DATA:
        teacher_user, _ = User.objects.get_or_create(
            username=email.split('@')[0],
            defaults={
                'email': email,
                'first_name': first,
                'last_name': last,
                'password': make_password(DEFAULT_TEACHER_PASSWORD),
                'role': User.Role.TEACHER,
                'is_2fa_enabled': False,
            }
        )
        if teacher_user.role != User.Role.TEACHER:
            teacher_user.role = User.Role.TEACHER
            teacher_user.save(update_fields=['role'])

        prof, _ = Professor.objects.get_or_create(
            email=email,
            defaults={'user': teacher_user, 'first_name': first, 'last_name': last, 'specialization': spec}
        )
        if prof.user_id is None:
            prof.user = teacher_user
            prof.save(update_fields=['user'])
        profesores.append(prof)

    # 2. CREAR AULAS
    print("Creando aulas...")
    aulas = []
    for code, building, floor, capacity, is_lab in AULAS_DATA:
        aula, _ = Classroom.objects.get_or_create(
            code=code,
            defaults={'building': building, 'floor': floor, 'capacity': capacity, 'is_lab': is_lab}
        )
        aulas.append(aula)

    # 3. CREAR MATERIAS
    print("Creando materias de primer nivel...")
    materias_creadas = []
    for code, name, credits, semester, carrera in MATERIAS_DATA:
        materia, _ = Subject.objects.get_or_create(
            code=code,
            defaults={'name': name, 'credits': credits, 'semester': semester, 'carrera': carrera}
        )
        materias_creadas.append(materia)

    # 4. CREAR HORARIOS (1 por cada materia)
    print("Asignando horarios a materias...")
    horarios = []
    for i, materia in enumerate(materias_creadas):
        dia = DIAS[i % len(DIAS)]
        inicio = HORARIOS_INICIO[i % len(HORARIOS_INICIO)]
        fin = time(inicio.hour + 2, 0)
        profesor = profesores[i % len(profesores)]
        aula = aulas[i % len(aulas)]

        horario, _ = Schedule.objects.get_or_create(
            subject=materia,
            professor=profesor,
            day_of_week=dia,
            academic_period=PERIODO_ACTUAL,
            defaults={'classroom': aula, 'start_time': inicio, 'end_time': fin}
        )
        horarios.append(horario)

    # 5. CREAR 100 ESTUDIANTES
    print(f"\nGenerando 100 estudiantes de Primer Nivel ({PERIODO_ACTUAL})...")
    
    # Crear al menos a Nick Bryan Lopez Reina como usuario principal de prueba
    nick_user, _ = User.objects.get_or_create(
        username='nlopezr',
        defaults={
            'email': 'nlopezr@pucesi.edu.ec',
            'first_name': 'Nick Bryan',
            'last_name': 'Lopez Reina',
            'password': make_password(DEFAULT_STUDENT_PASSWORD),
            'role': User.Role.STUDENT,
            'is_2fa_enabled': False,
        }
    )
    
    nick_student, _ = Student.objects.get_or_create(
        user=nick_user,
        defaults={
            'student_code': 'EST-NICK',
            'carrera': 'CIV',  # Nick en Civil
            'semester_current': 1,
            'career_start_date': date(2026, 3, 1),
        }
    )

    estudiantes_generados = [nick_student]
    
    for i in range(2, 101):
        nombre = random.choice(NOMBRES)
        apellido1 = random.choice(APELLIDOS)
        apellido2 = random.choice(APELLIDOS)
        codigo = f"EST-{i:03d}"
        username = f"est{i:03d}"
        email = f"{username}@pucesi.edu.ec"
        carrera_asignada = random.choice(CARRERAS)

        user, _ = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'first_name': nombre,
                'last_name': f"{apellido1} {apellido2}",
                'password': make_password(DEFAULT_STUDENT_PASSWORD),
                'role': User.Role.STUDENT,
                'is_2fa_enabled': False,
            }
        )

        student, _ = Student.objects.get_or_create(
            user=user,
            defaults={
                'student_code': codigo,
                'carrera': carrera_asignada,
                'semester_current': 1,
                'career_start_date': date(2026, 3, 1),
            }
        )
        estudiantes_generados.append(student)

    # 6. MATRICULAR Y ASIGNAR NOTAS EN CURSO
    print("Matriculando estudiantes en sus respectivas materias...")
    for student in estudiantes_generados:
        # Encontrar materias de su carrera
        materias_carrera = [m for m in materias_creadas if m.carrera == student.carrera]
        
        for materia in materias_carrera:
            # Buscar horario correspondiente
            horario = next((h for h in horarios if h.subject == materia), None)
            
            if horario:
                Enrollment.objects.get_or_create(
                    student=student,
                    schedule=horario,
                    academic_period=PERIODO_ACTUAL,
                    status='active'
                )

            # Asignar calificaciones "en curso" (solo parcial 1, el resto en blanco)
            Grade.objects.get_or_create(
                student=student,
                subject=materia,
                academic_period=PERIODO_ACTUAL,
                defaults={
                    'partial_1': Decimal(str(round(random.uniform(30.0, 50.0), 2))),
                    'partial_2': None,
                    'partial_3': None,
                    'final_exam': None,
                    'status': 'pending'
                }
            )

    print("\n" + "=" * 60)
    print("SEED DE PRIMER NIVEL COMPLETADO CON ÉXITO")
    print(f"Estudiantes generados: {len(estudiantes_generados)}")
    print(f"Materias creadas: {len(materias_creadas)}")
    print("\nUsuario de prueba principal:")
    print("   Usuario: nlopezr")
    print("   Clave:   [SEED_STUDENT_PASSWORD o clave temporal aleatoria]")
    print("   Docente: mandrade / [SEED_TEACHER_PASSWORD o clave temporal aleatoria]")
    print("=" * 60)

if __name__ == '__main__':
    run()
