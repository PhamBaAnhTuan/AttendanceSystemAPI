# face_recog/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FaceTrainingAPIView, AttendanceViewSet

router = DefaultRouter()
router.register(r'face', FaceTrainingAPIView, basename='face')
router.register(r'attendance', AttendanceViewSet, basename='attendance')

urlpatterns = [
    path('', include(router.urls)),
]