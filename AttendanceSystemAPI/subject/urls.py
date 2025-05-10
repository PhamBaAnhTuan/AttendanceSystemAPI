from rest_framework import routers
from django.urls import path, include
from .views import (
   SubjectViewSet, TeacherViewSet, StudentViewSet, ClassViewSet, RoomViewSet,
   ClassTeacherViewSet, ClassSubjectViewSet, ClassRoomViewSet, TeacherSubjectViewSet, StudentSubjectViewSet, RoomSubjectViewSet
)

router = routers.DefaultRouter()
router.register(r'subjects', SubjectViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'students', StudentViewSet)
router.register(r'classes', ClassViewSet)
router.register(r'rooms', RoomViewSet)
#
router.register(r'class-subject', ClassSubjectViewSet) 
router.register(r'class-teacher', ClassTeacherViewSet)
router.register(r'class-room', ClassRoomViewSet)
router.register(r'teacher-subject', TeacherSubjectViewSet)
router.register(r'student-subject', StudentSubjectViewSet)
router.register(r'room-subject', RoomSubjectViewSet)

urlpatterns = [
   path('', include(router.urls)),
]
