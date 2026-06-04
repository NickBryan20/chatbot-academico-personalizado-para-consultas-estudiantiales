"""
Script para poblar la base de datos con 100 estudiantes simulados.
Incluye: usuarios, perfiles académicos, materias, profesores, aulas,
horarios, matrículas y notas por parciales.

Uso:
    python manage.py runscript seed_database
    -- o --
    python scripts/seed_database.py
"""
import os
import sys
import django
import random
import secrets
from datetime import date, time, timedelta
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
DEFAULT_ADMIN_PASSWORD = settings.SEED_ADMIN_PASSWORD or secrets.token_urlsafe(12)

# ─── DATOS BASE ─────────────────────────────────────────────────────────────

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
]

MATERIAS_IDS = [
    # (código, nombre, créditos, semestre)
    ('IDS-101', 'Fundamentos de Programación', 4, 1),
    ('IDS-102', 'Matemáticas Discretas', 4, 1),
    ('IDS-103', 'Introducción a la Ingeniería de Software', 3, 1),
    ('IDS-104', 'Cálculo Diferencial', 4, 1),
    ('IDS-201', 'Programación Orientada a Objetos', 4, 2),
    ('IDS-202', 'Álgebra Lineal', 4, 2),
    ('IDS-203', 'Bases de Datos I', 4, 2),
    ('IDS-204', 'Sistemas Operativos', 3, 2),
    ('IDS-301', 'Bases de Datos II', 4, 3),
    ('IDS-302', 'Estructuras de Datos', 4, 3),
    ('IDS-303', 'Redes de Computadoras', 4, 3),
    ('IDS-304', 'Ingeniería de Software I', 3, 3),
    ('IDS-401', 'Desarrollo Web Frontend', 4, 4),
    ('IDS-402', 'Desarrollo Web Backend', 4, 4),
    ('IDS-403', 'Inteligencia Artificial', 4, 4),
    ('IDS-404', 'Seguridad Informática', 3, 4),
    ('IDS-501', 'Arquitectura de Software', 4, 5),
    ('IDS-502', 'Computación en la Nube', 4, 5),
    ('IDS-503', 'Desarrollo de Aplicaciones Móviles', 4, 5),
    ('IDS-504', 'Gestión de Proyectos TI', 3, 5),
]

AULAS_DATA = [
    ('A-101', 'A', 1, 35, False),
    ('A-102', 'A', 1, 35, False),
    ('A-201', 'A', 2, 40, False),
    ('A-202', 'A', 2, 40, False),
    ('B-101', 'B', 1, 30, False),
    ('B-102', 'B', 1, 30, False),
    ('B-201', 'B', 2, 35, False),
    ('LAB-01', 'LAB', 1, 25, True),
    ('LAB-02', 'LAB', 1, 25, True),
    ('LAB-03', 'LAB', 2, 20, True),
]

DIAS = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
HORARIOS_INICIO = [time(7, 0), time(9, 0), time(11, 0), time(14, 0), time(16, 0)]
PERIODO_ACTUAL = '2024-2025-II'


def run():
    print("Iniciando seed de base de datos...")
    print("=" * 60)

    # ─── 1. CREAR PROFESORES ────────────────────────────────────────
    print("\nCreando profesores...")
    profesores = []
    for first, last, email, spec in PROFESORES_DATA:
        prof, created = Professor.objects.get_or_create(
            email=email,
            defaults={
                'first_name': first,
                'last_name': last,
                'specialization': spec,
            }
        )
        profesores.append(prof)
        if created:
            print(f"  OK: Prof. {first} {last}")

    # ─── 2. CREAR AULAS ─────────────────────────────────────────────
    print("\nCreando aulas...")
    aulas = []
    for code, building, floor, capacity, is_lab in AULAS_DATA:
        aula, created = Classroom.objects.get_or_create(
            code=code,
            defaults={
                'building': building,
                'floor': floor,
                'capacity': capacity,
                'is_lab': is_lab,
            }
        )
        aulas.append(aula)
        if created:
            print(f"  OK: Aula {code}")

    # ─── 3. CREAR MATERIAS ──────────────────────────────────────────
    print("\nCreando materias...")
    materias = []
    for code, name, credits, semester in MATERIAS_IDS:
        materia, created = Subject.objects.get_or_create(
            code=code,
            defaults={
                'name': name,
                'credits': credits,
                'semester': semester,
                'carrera': 'IDS',
            }
        )
        materias.append(materia)
        if created:
            print(f"  OK: {code} - {name}")

    # ─── 4. CREAR HORARIOS ──────────────────────────────────────────
    print("\nCreando horarios...")
    horarios = []
    for i, materia in enumerate(materias[:10]):  # 10 materias | horarios base
        dia = DIAS[i % len(DIAS)]
        inicio = HORARIOS_INICIO[i % len(HORARIOS_INICIO)]
        fin = time(inicio.hour + 2, 0)
        profesor = profesores[i % len(profesores)]
        aula = aulas[i % len(aulas)]

        horario, created = Schedule.objects.get_or_create(
            subject=materia,
            professor=profesor,
            day_of_week=dia,
            academic_period=PERIODO_ACTUAL,
            defaults={
                'classroom': aula,
                'start_time': inicio,
                'end_time': fin,
            }
        )
        horarios.append(horario)
        if created:
            print(f"  OK: {materia.name} - {dia} {inicio}")

    # ─── 5. CREAR 100 ESTUDIANTES ───────────────────────────────────
    print("\nCreando 100 estudiantes simulados...")
    estudiantes_creados = 0
    semestres_posibles = [1, 2, 3, 4, 5]

    for i in range(1, 101):
        nombre = random.choice(NOMBRES)
        apellido1 = random.choice(APELLIDOS)
        apellido2 = random.choice(APELLIDOS)
        codigo = f"EST-{i:03d}"
        username = f"est{i:03d}"
        email = f"{username}@pucesi.edu.ec"
        semestre = random.choice(semestres_posibles)

        # Calcular fecha de inicio de carrera según semestre
        años_atras = (semestre - 1) // 2
        fecha_inicio = date(2024 - años_atras, 3, 1)

        # Crear usuario
        user, user_created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'first_name': nombre,
                'last_name': f"{apellido1} {apellido2}",
                'password': make_password(DEFAULT_STUDENT_PASSWORD),
                'is_2fa_enabled': True,
            }
        )

        # Crear perfil de estudiante
        student, student_created = Student.objects.get_or_create(
            user=user,
            defaults={
                'student_code': codigo,
                'carrera': 'IDS',
                'semester_current': semestre,
                'career_start_date': fecha_inicio,
            }
        )

        if student_created:
            estudiantes_creados += 1

            # Materias del semestre actual y el anterior (si existe)
            materias_del_semestre = [m for m in materias if m.semester in [semestre, max(1, semestre-1)]]
            if not materias_del_semestre:
                materias_del_semestre = materias[:4]

            # Seleccionar entre 4-6 materias
            materias_seleccionadas = random.sample(
                materias_del_semestre,
                min(len(materias_del_semestre), random.randint(4, 6))
            )

            # Crear matrículas y notas
            for materia in materias_seleccionadas:
                # Buscar horario compatible
                horario_compatible = next(
                    (h for h in horarios if h.subject == materia), None
                )

                if horario_compatible:
                    Enrollment.objects.get_or_create(
                        student=student,
                        schedule=horario_compatible,
                        academic_period=PERIODO_ACTUAL,
                    )

                # Crear notas (con variación realista)
                p1 = Decimal(str(round(random.uniform(5.5, 10.0), 2)))
                p2 = Decimal(str(round(random.uniform(5.5, 10.0), 2)))
                p3_val = random.uniform(5.5, 10.0) if semestre > 1 else None
                p3 = Decimal(str(round(p3_val, 2))) if p3_val else None

                Grade.objects.get_or_create(
                    student=student,
                    subject=materia,
                    academic_period=PERIODO_ACTUAL,
                    defaults={
                        'partial_1': p1,
                        'partial_2': p2,
                        'partial_3': p3,
                    }
                )

        if i % 20 == 0:
            print(f"  Progreso: {i}/100 estudiantes procesados...")

    # ─── 6. CREAR SUPERUSUARIO ──────────────────────────────────────
    print("\nCreando administrador...")
    admin, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@pucesi.edu.ec',
            'first_name': 'Administrador',
            'last_name': 'PUCESI',
            'is_staff': True,
            'is_superuser': True,
            'is_2fa_enabled': False,
            'password': make_password(DEFAULT_ADMIN_PASSWORD),
        }
    )
    if created:
        print("  OK: Admin creado.")

    # ─── RESUMEN ────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("SEED COMPLETADO")
    print(f"   Estudiantes creados: {estudiantes_creados}")
    print(f"   Materias: {Subject.objects.count()}")
    print(f"   Profesores: {Professor.objects.count()}")
    print(f"   Aulas: {Classroom.objects.count()}")
    print(f"   Notas registradas: {Grade.objects.count()}")
    print(f"   Horarios: {Schedule.objects.count()}")
    print("\nCredenciales de prueba:")
    print("   Estudiante: est001 / [SEED_STUDENT_PASSWORD o clave temporal aleatoria]")
    print("   Admin:      admin  / [SEED_ADMIN_PASSWORD o clave temporal aleatoria]")
    print("=" * 60)


if __name__ == '__main__':
    run()
