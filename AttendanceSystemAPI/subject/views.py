from rest_framework import viewsets
from .models import (
   Faculty, Major,
   Subject, Class, Room,
   TeacherMajor, TeacherClass, TeacherSubject,
   Schedule, PeriodDefinition,
)
from user.models import User

from .serializers import (
   FacultySerializer,
   MajorSerializer,
   SubjectSerializer,
   ClassSerializer,
   RoomSerializer,

   TeacherMajorSerializer,
   
   TeacherSubjectSerializer,
   
   TeacherClassSerializer,
   
   ScheduleSerializer,
   PeriodDefinitionSerializer
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
# permission
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from oauth2_provider.contrib.rest_framework.permissions import OAuth2Authentication
# filter
from .filter import TeacherFilterBackend, ScheduleFilterBackend
# 
from oauth2_provider.views.mixins import OAuthLibMixin
from AttendanceSystemAPI.views.base import BaseViewSet

class FacultyViewSet(BaseViewSet, OAuthLibMixin):
   queryset = Faculty.objects.all()
   serializer_class = FacultySerializer
   required_alternate_scopes = {
      "list": [["admin"], ["teacher"], ["student"]],
      "retrieve": [["admin"], ["teacher"], ["student"]],
      "create": [["admin"]],
      "update": [["admin"]],
      "destroy": [["admin"]],
   }
class MajorViewSet(viewsets.ModelViewSet):
   queryset = Major.objects.all()
   serializer_class = MajorSerializer
   filter_backends=[TeacherFilterBackend]
   required_alternate_scopes = {
      "list": [["admin"], ["teacher"], ["student"]],
      "retrieve": [["admin"], ["teacher"], ["student"]],
      "create": [["admin"]],
      "update": [["admin"]],
      "destroy": [["admin"]],
   }
class SubjectViewSet(viewsets.ModelViewSet):
   queryset = Subject.objects.all()
   serializer_class = SubjectSerializer
   required_alternate_scopes = {
      "list": [["admin"], ["teacher"], ["student"]],
      "retrieve": [["admin"], ["teacher"], ["student"]],
      "create": [["admin"]],
      "update": [["admin"]],
      "destroy": [["admin"]],
   }
class ClassViewSet(viewsets.ModelViewSet):
   queryset = Class.objects.all()
   serializer_class = ClassSerializer
   filter_backends=[TeacherFilterBackend]
   required_alternate_scopes = {
      "list": [["admin"], ["teacher"], ["student"]],
      "retrieve": [["admin"], ["teacher"], ["student"]],
      "create": [["admin"]],
      "update": [["admin"]],
      "destroy": [["admin"]],
   }
class RoomViewSet(viewsets.ModelViewSet):
   queryset = Room.objects.all()
   serializer_class = RoomSerializer
   required_alternate_scopes = {
      "list": [["admin"], ["teacher"], ["student"]],
      "retrieve": [["admin"], ["teacher"], ["student"]],
      "create": [["admin"]],
      "update": [["admin"]],
      "destroy": [["admin"]],
   }
   
class TeacherMajorViewSet(viewsets.ModelViewSet):
   queryset = TeacherMajor.objects.all()
   serializer_class = TeacherMajorSerializer
   filter_backends=[TeacherFilterBackend]
   required_alternate_scopes = {
      "list": [["admin"], ["teacher"]],
      "retrieve": [["admin"], ["teacher"]],
      "create": [["admin"]],
      "update": [["admin"]],
      "destroy": [["admin"]],
   }
class TeacherSubjectViewSet(viewsets.ModelViewSet):
   queryset = TeacherSubject.objects.all()
   serializer_class = TeacherSubjectSerializer
   filter_backends=[TeacherFilterBackend]
   required_alternate_scopes = {
      "list": [["admin"], ["teacher"]],
      "retrieve": [["admin"], ["teacher"]],
      "create": [["admin"]],
      "update": [["admin"]],
      "destroy": [["admin"]],
   }
   def create(self, request, *args, **kwargs):
      many = isinstance(request.data, list)
      serializer = self.get_serializer(data=request.data, many=many)
      serializer.is_valid(raise_exception=True)
      self.perform_create(serializer)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
   
class TeacherClassViewSet(viewsets.ModelViewSet):
   queryset = TeacherClass.objects.all()
   serializer_class = TeacherClassSerializer
   filter_backends=[TeacherFilterBackend]
   required_alternate_scopes = {
      "list": [["admin"], ["teacher"]],
      "retrieve": [["admin"], ["teacher"]],
      "create": [["admin"]],
      "update": [["admin"]],
      "destroy": [["admin"]],
   }
   def create(self, request, *args, **kwargs):
      many = isinstance(request.data, list)
      serializer = self.get_serializer(data=request.data, many=many)
      serializer.is_valid(raise_exception=True)
      self.perform_create(serializer)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
class PeriodDefinitionViewSet(viewsets.ModelViewSet):
   queryset = PeriodDefinition.objects.all()
   serializer_class = PeriodDefinitionSerializer
   filter_backends=[ScheduleFilterBackend]
   required_alternate_scopes = {
      "list": [["admin"], ["teacher"], ["student"]],
      "retrieve": [["admin"], ["teacher"], ["student"]],
      "create": [["admin"]],
      "update": [["admin"]],
      "destroy": [["admin"]],
   }
   
   def create(self, request, *args, **kwargs):
      is_many = isinstance(request.data, list)
   
      serializer = self.get_serializer(data=request.data, many=is_many)
      serializer.is_valid(raise_exception=True)
      self.perform_create(serializer)
   
      headers = self.get_success_headers(serializer.data if not is_many else serializer.data[0])
      return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
class ScheduleViewSet(viewsets.ModelViewSet):
   queryset = Schedule.objects.all()
   serializer_class = ScheduleSerializer
   filter_backends=[ScheduleFilterBackend]
   required_alternate_scopes = {
      "list": [["admin"], ["teacher"], ["student"]],
      "retrieve": [["admin"], ["teacher"], ["student"]],
      "create": [["admin"]],
      "update": [["admin"]],
      "destroy": [["admin"]],
   }


# @action(detail=False, methods=['post'], url_path='upload-image')
   # def upload_image(self, request):
   #    image = request.FILES.get('image')
   #    if not image:
   #       return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)

   #    # Đặt tên file dựa trên tên file gửi lên từ frontend
   #    filename = image.name  # ví dụ: 123_NguyenVanA_front.jpg

   #    # Thư mục lưu ảnh (media/student_images/)
   #    save_path = os.path.join('teacher_images', filename)
   #    full_path = os.path.join(settings.MEDIA_ROOT, save_path)

   #    # Đảm bảo thư mục tồn tại
   #    os.makedirs(os.path.dirname(full_path), exist_ok=True)

   #    # Ghi file
   #    with default_storage.open(save_path, 'wb+') as destination:
   #       for chunk in image.chunks():
   #             destination.write(chunk)

   #    return Response({'message': 'Image saved successfully', 'path': settings.MEDIA_URL + save_path})
   
#    @action(detail=False, methods=['delete'], url_path='delete-by-param')
#    def delete_by_param(self, request):
#       teacher_id = request.query_params.get('teacher_id')
#       subject_id = request.query_params.get('subject_id')

#       if teacher_id and subject_id:
#          qs = TeacherSubject.objects.filter(teacher_id=teacher_id, subject_id=subject_id)
#          deleted_count = qs.count()
#          if deleted_count == 0:
#                return Response({"detail": "No matching records found."}, status=status.HTTP_404_NOT_FOUND)
#          qs.delete()
#          return Response({"detail": f"deleted relation between teacher_id: {teacher_id} and subject_id: {subject_id}."}, status=status.HTTP_204_NO_CONTENT)

#       return Response({"detail": "teacher_id and subject_id are required."}, status=status.HTTP_400_BAD_REQUEST)