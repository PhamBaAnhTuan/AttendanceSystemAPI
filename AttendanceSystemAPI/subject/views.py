from rest_framework import viewsets
from .models import (
   Faculty, Major,
   Subject, Class, Room,
   TeacherMajor, TeacherClass, TeacherSubject, TeacherClassSubject,
   StudentClass,
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
   TeacherClassSubjectSerializer,
   
   StudentClassSerializer,
   
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
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
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
   def get_queryset(self):
      user = self.request.user
      if not user or not user.is_authenticated:
         raise NotAuthenticated("You must be signin in to access this resource!")
      if not hasattr(user, 'role') or user.role is None:
         raise PermissionDenied("You do not have a role assigned!")
      if user.role.name == "admin":
         return Faculty.objects.all()
      return Faculty.objects.filter(teacher_id=user.id)
class MajorViewSet(BaseViewSet, OAuthLibMixin):
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
   def get_queryset(self):
      user = self.request.user
      if not user or not user.is_authenticated:
         raise NotAuthenticated("You must be signin in to access this resource!")
      if not hasattr(user, 'role') or user.role is None:
         raise PermissionDenied("You do not have a role assigned!")
      if user.role.name == "admin":
         return Major.objects.all()
      return Major.objects.filter(teacher_id=user.id)
class SubjectViewSet(BaseViewSet, OAuthLibMixin):
   queryset = Subject.objects.all()
   serializer_class = SubjectSerializer
   filter_backends=[TeacherFilterBackend]
   required_alternate_scopes = {
      "list": [["admin"], ["teacher"], ["student"]],
      "retrieve": [["admin"], ["teacher"], ["student"]],
      "create": [["admin"]],
      "update": [["admin"]],
      "destroy": [["admin"]],
   }
   def get_queryset(self):
      user = self.request.user
      if not user or not user.is_authenticated:
         raise NotAuthenticated("You must be signin in to access this resource!")
      if not hasattr(user, 'role') or user.role is None:
         raise PermissionDenied("You do not have a role assigned!")
      if user.role.name == "admin":
         return Subject.objects.all()
      return Subject.objects.filter(teacher_id=user.id)
class ClassViewSet(BaseViewSet, OAuthLibMixin):
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
   def get_queryset(self):
      user = self.request.user
      if not user or not user.is_authenticated:
            raise NotAuthenticated("You must be signin in to access this resource!")
      if not hasattr(user, 'role') or user.role is None:
            raise PermissionDenied("You do not have a role assigned!")
      if user.role.name == "admin":
            return Class.objects.all()
      return Class.objects.filter(teacher_id=user.id)
class RoomViewSet(BaseViewSet, OAuthLibMixin):
   queryset = Room.objects.all()
   serializer_class = RoomSerializer
   required_alternate_scopes = {
      "list": [["admin"], ["teacher"], ["student"]],
      "retrieve": [["admin"], ["teacher"], ["student"]],
      "create": [["admin"]],
      "update": [["admin"]],
      "destroy": [["admin"]],
   }
   def get_queryset(self):
      user = self.request.user
      if not user or not user.is_authenticated:
         raise NotAuthenticated("You must be signin in to access this resource!")
      if not hasattr(user, 'role') or user.role is None:
         raise PermissionDenied("You do not have a role assigned!")
      if user.role.name == "admin":
         return Room.objects.all()
      return Room.objects.filter(teacher_id=user.id)
   
class TeacherMajorViewSet(BaseViewSet, OAuthLibMixin):
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
   def get_queryset(self):
      user = self.request.user
      if not user or not user.is_authenticated:
         raise NotAuthenticated("You must be signin in to access this resource!")
      if not hasattr(user, 'role') or user.role is None:
         raise PermissionDenied("You do not have a role assigned!")
      if user.role.name == "admin":
         return TeacherMajor.objects.all()
      return TeacherMajor.objects.filter(teacher_id=user.id)
class TeacherSubjectViewSet(BaseViewSet, OAuthLibMixin):
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
   def get_queryset(self):
        user = self.request.user
        if not user or not user.is_authenticated:
            raise NotAuthenticated("You must be signin in to access this resource!")
        if not hasattr(user, 'role') or user.role is None:
            raise PermissionDenied("You do not have a role assigned!")
        if user.role.name == "admin":
            return TeacherSubject.objects.all()
        return TeacherSubject.objects.filter(teacher_id=user.id)
     
   def create(self, request, *args, **kwargs):
      many = isinstance(request.data, list)
      serializer = self.get_serializer(data=request.data, many=many)
      serializer.is_valid(raise_exception=True)
      self.perform_create(serializer)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
   
   @action(detail=False, methods=['delete'], url_path='delete-by-param', permission_classes=[IsAuthenticated])
   def delete_by_param(self, request):
      teacher_id = request.query_params.get('teacher_id')
      subject_id = request.query_params.get('subject_id')

      if teacher_id and subject_id:
         qs = TeacherSubject.objects.filter(teacher_id=teacher_id, subject_id=subject_id)
         deleted_count = qs.count()
         if deleted_count == 0:
               return Response({"detail": "No matching records found."}, status=status.HTTP_404_NOT_FOUND)
         qs.delete()
         return Response({"detail": f"deleted relation between teacher_id: {teacher_id} \nand subject_id: {subject_id}."}, status=status.HTTP_204_NO_CONTENT)

      return Response({"detail": "teacher_id and subject_id are required."}, status=status.HTTP_400_BAD_REQUEST)
   
class TeacherClassViewSet(BaseViewSet, OAuthLibMixin):
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
   def get_queryset(self):
      user = self.request.user
      if not user or not user.is_authenticated:
         raise NotAuthenticated("You must be signin in to access this resource!")
      if not hasattr(user, 'role') or user.role is None:
         raise PermissionDenied("You do not have a role assigned!")
      if user.role.name == "admin":
         return TeacherClass.objects.all()
      return TeacherClass.objects.filter(teacher_id=user.id)
     
   def create(self, request, *args, **kwargs):
      many = isinstance(request.data, list)
      serializer = self.get_serializer(data=request.data, many=many)
      serializer.is_valid(raise_exception=True)
      self.perform_create(serializer)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
   
   @action(detail=False, methods=['delete'], url_path='delete-by-param', permission_classes=[IsAuthenticated])
   def delete_by_param(self, request):
      teacher_id = request.query_params.get('teacher_id')
      class_id = request.query_params.get('class_id')

      if teacher_id and class_id:
         qs = TeacherClass.objects.filter(teacher_id=teacher_id, classes_id=class_id)
         deleted_count = qs.count()
         if deleted_count == 0:
               return Response({"detail": "No matching records found."}, status=status.HTTP_404_NOT_FOUND)
         qs.delete()
         return Response({"detail": f"deleted relation between teacher_id: {teacher_id} \nand class_id: {class_id}."}, status=status.HTTP_204_NO_CONTENT)

      return Response({"detail": "teacher_id and class_id are required."}, status=status.HTTP_400_BAD_REQUEST)

# 
class TeacherClassSubjectViewSet(BaseViewSet, OAuthLibMixin):
   queryset = TeacherClassSubject.objects.all()
   serializer_class = TeacherClassSubjectSerializer
   filter_backends=[TeacherFilterBackend]
   required_alternate_scopes = {
      "list": [["admin"], ["teacher"]],
      "retrieve": [["admin"], ["teacher"]],
      "create": [["admin"]],
      "update": [["admin"]],
      "destroy": [["admin"]],
   }
   def get_queryset(self):
      user = self.request.user
      if not user or not user.is_authenticated:
         raise NotAuthenticated("You must be signin in to access this resource!")
      if not hasattr(user, 'role') or user.role is None:
         raise PermissionDenied("You do not have a role assigned!")
      if user.role.name == "admin":
         return TeacherClassSubject.objects.all()
      return TeacherClassSubject.objects.filter(teacher_id=user.id)
     
   def create(self, request, *args, **kwargs):
      many = isinstance(request.data, list)
      serializer = self.get_serializer(data=request.data, many=many)
      serializer.is_valid(raise_exception=True)
      self.perform_create(serializer)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
   
   @action(detail=False, methods=['delete'], url_path='delete-by-param', permission_classes=[IsAuthenticated])
   def delete_by_param(self, request):
      teacher_id = request.query_params.get('teacher_id')
      class_id = request.query_params.get('class_id')
      subject_id = request.query_params.get('subject_id')

      if teacher_id and class_id:
         qs = TeacherClassSubject.objects.filter(teacher_id=teacher_id, classes_id=class_id, subject_id=subject_id)
         deleted_count = qs.count()
         if deleted_count == 0:
               return Response({"detail": "No matching records found."}, status=status.HTTP_404_NOT_FOUND)
         qs.delete()
         return Response(
            {"detail": f"deleted relation between teacher_id: {teacher_id} \nand class_id: {class_id} \nand subject_id: {subject_id}."},
            status=status.HTTP_204_NO_CONTENT
         )

      return Response({"detail": "teacher_id and class_id are required."}, status=status.HTTP_400_BAD_REQUEST)
   # 
   # 
class StudentClassViewSet(BaseViewSet, OAuthLibMixin):
   queryset = StudentClass.objects.all()
   serializer_class = StudentClassSerializer
   filter_backends=[TeacherFilterBackend]
   required_alternate_scopes = {
      "list": [["admin"], ["teacher"]],
      "retrieve": [["admin"], ["teacher"]],
      "create": [["admin"]],
      "update": [["admin"]],
      "destroy": [["admin"]],
   }
   def get_queryset(self):
      user = self.request.user
      if not user or not user.is_authenticated:
         raise NotAuthenticated("You must be signin in to access this resource!")
      if not hasattr(user, 'role') or user.role is None:
         raise PermissionDenied("You do not have a role assigned!")
      if user.role.name == "admin":
         return StudentClass.objects.all()
      return StudentClass.objects.filter(student_id=user.id)
     
   def create(self, request, *args, **kwargs):
      many = isinstance(request.data, list)
      serializer = self.get_serializer(data=request.data, many=many)
      serializer.is_valid(raise_exception=True)
      self.perform_create(serializer)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
   @action(detail=False, methods=['delete'], url_path='delete-by-param', permission_classes=[IsAuthenticated])
   def delete_by_param(self, request):
      student_id = request.query_params.get('student_id')
      class_id = request.query_params.get('class_id')

      if student_id and class_id:
         qs = StudentClass.objects.filter(student_id=student_id, classes_id=class_id)
         deleted_count = qs.count()
         if deleted_count == 0:
               return Response({"detail": "No matching records found."}, status=status.HTTP_404_NOT_FOUND)
         qs.delete()
         return Response(
            {"detail": f"deleted relation between student_id: {student_id} \nand class_id: {class_id}."},
            status=status.HTTP_204_NO_CONTENT
         )

      return Response({"detail": "student_id and class_id are required."}, status=status.HTTP_400_BAD_REQUEST)
   
class PeriodDefinitionViewSet(BaseViewSet, OAuthLibMixin):
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
class ScheduleViewSet(BaseViewSet, OAuthLibMixin):
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