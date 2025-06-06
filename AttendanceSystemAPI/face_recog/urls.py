# face_recog/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AttendanceViewSet, FaceTrainingAPIView

router = DefaultRouter()
router.register(r'face_training', FaceTrainingAPIView, basename='face_training')
router.register(r'attendance', AttendanceViewSet, basename='attendance')
# router.register(r'', AttendanceViewSet, basename='attendance')

urlpatterns = [
   path('', include(router.urls)),
]