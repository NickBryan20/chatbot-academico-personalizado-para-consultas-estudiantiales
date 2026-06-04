"""Serializers para el módulo de estudiantes."""
from rest_framework import serializers
from .models import Student, Subject, Professor, Classroom, Schedule, Enrollment, Grade, Notification, Activity, ActivitySubmission


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = ['id', 'full_name', 'email', 'specialization']


class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = '__all__'


class ScheduleSerializer(serializers.ModelSerializer):
    subject_details = SubjectSerializer(source='subject', read_only=True)
    professor_details = ProfessorSerializer(source='professor', read_only=True)
    classroom_details = ClassroomSerializer(source='classroom', read_only=True)
    day_display = serializers.CharField(source='get_day_of_week_display', read_only=True)

    class Meta:
        model = Schedule
        fields = ['id', 'subject_details', 'professor_details', 'classroom_details', 
                  'day_of_week', 'day_display', 'start_time', 'end_time', 'academic_period']


class GradeSerializer(serializers.ModelSerializer):
    subject_name = serializers.ReadOnlyField(source='subject.name')
    subject_code = serializers.ReadOnlyField(source='subject.code')

    class Meta:
        model = Grade
        fields = ['id', 'subject_name', 'subject_code', 'academic_period', 
                  'partial_1', 'partial_2', 'partial_3', 'final_exam', 'final_grade', 
                  'attendance_percentage', 'status']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class StudentProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    email = serializers.ReadOnlyField()
    carrera_display = serializers.CharField(source='get_carrera_display', read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'student_code', 'full_name', 'email', 'carrera', 
                  'carrera_display', 'semester_current', 'career_start_date', 'photo']


class ActivitySubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivitySubmission
        fields = '__all__'
        read_only_fields = ['student', 'activity', 'submitted_at']


class ActivitySerializer(serializers.ModelSerializer):
    subject_name = serializers.ReadOnlyField(source='subject.name')
    submission = serializers.SerializerMethodField()
    
    class Meta:
        model = Activity
        fields = ['id', 'subject', 'subject_name', 'title', 'description', 'due_date', 'file', 'created_at', 'submission']
        
    def get_submission(self, obj):
        request = self.context.get('request')
        if request and request.user and hasattr(request.user, 'student_profile'):
            submission = ActivitySubmission.objects.filter(activity=obj, student=request.user.student_profile).first()
            if submission:
                return ActivitySubmissionSerializer(submission).data
        return None
