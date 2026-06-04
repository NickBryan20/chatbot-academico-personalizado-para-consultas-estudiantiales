"""Views para el módulo de estudiantes: Enrutadores."""
from django.core.exceptions import PermissionDenied, ValidationError
from rest_framework import permissions, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Student, Notification, Professor
from .serializers import (
    StudentProfileSerializer, GradeSerializer, ScheduleSerializer, 
    NotificationSerializer, ActivitySerializer, ActivitySubmissionSerializer,
    ActivityCreateSerializer, SubjectSerializer
)
from .controllers import EstudianteControlador


class StudentProfileView(APIView):
    """Router: Obtiene el perfil del estudiante autenticado."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            student = EstudianteControlador.obtener_perfil(request.user, request)
            return Response(StudentProfileSerializer(student).data)
        except Student.DoesNotExist:
            return Response({'error': 'Perfil no encontrado.'}, status=status.HTTP_404_NOT_FOUND)


class StudentGradesView(APIView):
    """Router: Lista las notas del estudiante autenticado."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            period = request.query_params.get('period')
            grades = EstudianteControlador.obtener_calificaciones(request.user, period, request)
            serializer = GradeSerializer(grades, many=True)
            return Response({
                'period': period or 'Historial Completo',
                'grades': serializer.data
            })
        except Student.DoesNotExist:
            return Response({'error': 'Perfil no encontrado.'}, status=status.HTTP_404_NOT_FOUND)


class StudentScheduleView(APIView):
    """Router: Lista el horario de clases del estudiante."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            period = request.query_params.get('period', '2026-01')
            schedules = EstudianteControlador.obtener_horario(request.user, period, request)
            serializer = ScheduleSerializer(schedules, many=True)
            return Response({
                'period': period,
                'schedule': serializer.data
            })
        except Student.DoesNotExist:
            return Response({'error': 'Perfil no encontrado.'}, status=status.HTTP_404_NOT_FOUND)


class StudentStatsView(APIView):
    """Router: Estadísticas académicas."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            stats = EstudianteControlador.obtener_estadisticas(request.user)
            return Response(stats)
        except Student.DoesNotExist:
            return Response({'error': 'No encontrado.'}, status=404)


class NotificationListView(APIView):
    """Router: Notificaciones."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            unread_only = request.query_params.get('unread_only') == 'true'
            notifications = EstudianteControlador.obtener_notificaciones(request.user, unread_only)
            serializer = NotificationSerializer(notifications, many=True)
            return Response(serializer.data)
        except Student.DoesNotExist:
            return Response({'error': 'Perfil no encontrado.'}, status=status.HTTP_404_NOT_FOUND)


class NotificationMarkReadView(APIView):
    """Router: Marcar notificación como leída."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            EstudianteControlador.marcar_notificacion_leida(request.user, pk)
            return Response({'status': 'ok'})
        except (Student.DoesNotExist, Notification.DoesNotExist):
            return Response({'error': 'No encontrado.'}, status=404)


class ActivityListView(APIView):
    """Router: Lista las actividades/deberes del estudiante."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            activities = EstudianteControlador.obtener_actividades(request.user, request)
            serializer = ActivitySerializer(activities, many=True, context={'request': request})
            return Response(serializer.data)
        except Student.DoesNotExist:
            return Response({'error': 'Perfil no encontrado.'}, status=status.HTTP_404_NOT_FOUND)


class ActivitySubmitView(APIView):
    """Router: Envía o actualiza un deber."""
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, pk):
        try:
            file = request.FILES.get('file')
            comments = request.data.get('comments', '')
            if not file:
                return Response({'error': 'No se proporcionó ningún archivo.'}, status=status.HTTP_400_BAD_REQUEST)
                
            submission = EstudianteControlador.entregar_actividad(request.user, pk, file, comments, request)
            serializer = ActivitySubmissionSerializer(submission)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TeacherRequiredPermission(permissions.BasePermission):
    """Permite solo usuarios autenticados con rol docente."""

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and getattr(user, 'is_teacher', False)
        )


class TeacherSubjectListView(APIView):
    """Lista materias asignadas al docente autenticado."""
    permission_classes = [TeacherRequiredPermission]

    def get(self, request):
        try:
            subjects = EstudianteControlador.obtener_materias_docente(request.user)
            return Response(SubjectSerializer(subjects, many=True).data)
        except (Professor.DoesNotExist, PermissionDenied) as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)


class TeacherScheduleView(APIView):
    """Lista el horario del docente autenticado."""
    permission_classes = [TeacherRequiredPermission]

    def get(self, request):
        try:
            period = request.query_params.get('period', '2026-01')
            schedules = EstudianteControlador.obtener_horario_docente(request.user, period)
            serializer = ScheduleSerializer(schedules, many=True)
            return Response({'period': period, 'schedule': serializer.data})
        except (Professor.DoesNotExist, PermissionDenied) as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)


class TeacherActivityListCreateView(APIView):
    """Lista y crea actividades/tareas para materias del docente."""
    permission_classes = [TeacherRequiredPermission]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        try:
            activities = EstudianteControlador.obtener_actividades_docente(request.user)
            serializer = ActivitySerializer(activities, many=True, context={'request': request})
            return Response(serializer.data)
        except (Professor.DoesNotExist, PermissionDenied) as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        serializer = ActivityCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        try:
            activity = EstudianteControlador.crear_actividad_docente(
                request.user,
                serializer.validated_data,
                request.FILES.get('file'),
                request,
            )
            return Response(
                ActivitySerializer(activity, context={'request': request}).data,
                status=status.HTTP_201_CREATED,
            )
        except PermissionDenied as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
        except (Professor.DoesNotExist, ValidationError) as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
