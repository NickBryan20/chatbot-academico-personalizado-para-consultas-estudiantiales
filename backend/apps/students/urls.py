from django.urls import path
from .views import (
    StudentProfileView, StudentGradesView, StudentScheduleView, StudentStatsView,
    NotificationListView, NotificationMarkReadView, ActivityListView, ActivitySubmitView,
    TeacherSubjectListView, TeacherScheduleView, TeacherActivityListCreateView
)

urlpatterns = [
    path('profile/', StudentProfileView.as_view(), name='student-profile'),
    path('grades/', StudentGradesView.as_view(), name='student-grades'),
    path('schedule/', StudentScheduleView.as_view(), name='student-schedule'),
    path('stats/', StudentStatsView.as_view(), name='student-stats'),
    path('notifications/', NotificationListView.as_view(), name='student-notifications'),
    path('notifications/<uuid:pk>/read/', NotificationMarkReadView.as_view(), name='notification-read'),
    path('activities/', ActivityListView.as_view(), name='student-activities'),
    path('activities/<uuid:pk>/submit/', ActivitySubmitView.as_view(), name='activity-submit'),
    path('teacher/subjects/', TeacherSubjectListView.as_view(), name='teacher-subjects'),
    path('teacher/schedule/', TeacherScheduleView.as_view(), name='teacher-schedule'),
    path('teacher/activities/', TeacherActivityListCreateView.as_view(), name='teacher-activities'),
]
