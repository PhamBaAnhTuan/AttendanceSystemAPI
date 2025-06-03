from rest_framework import routers
from django.urls import path, include
from .views import (
   FacultyViewSet, MajorViewSet,
   SubjectViewSet, ClassViewSet, RoomViewSet,
   TeacherMajorViewSet, TeacherSubjectViewSet, TeacherClassViewSet, TeacherClassSubjectViewSet,
   StudentClassViewSet,
   ScheduleViewSet, PeriodDefinitionViewSet
)

router = routers.DefaultRouter()
router.register(r'faculty', FacultyViewSet)
router.register(r'major', MajorViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'classes', ClassViewSet)
router.register(r'rooms', RoomViewSet)
#
router.register(r'teacher-major', TeacherMajorViewSet)
router.register(r'teacher-subject', TeacherSubjectViewSet)
router.register(r'teacher-class', TeacherClassViewSet)

router.register(r'teacher-class-subject', TeacherClassSubjectViewSet)

router.register(r'student-class', StudentClassViewSet)

router.register(r'period', PeriodDefinitionViewSet)
router.register(r'schedule', ScheduleViewSet)

urlpatterns = [
   path('', include(router.urls)),
]
