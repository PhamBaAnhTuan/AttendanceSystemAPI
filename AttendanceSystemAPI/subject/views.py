from rest_framework import viewsets
from .models import Subject, Teacher, Student, Class, Room, ClassTeacher, ClassRoom, ClassSubject, TeacherSubject, StudentSubject, RoomSubject
from .serializers import (
   SubjectSerializer,
   TeacherSerializer,
   StudentSerializer,
   ClassSerializer,
   RoomSerializer,
   RoomSubjectSerializer,
   TeacherSubjectSerializer,
   StudentSubjectSerializer,
   ClassSubjectSerializer,
   ClassTeacherSerializer,
   ClassRoomSerializer
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

class SubjectViewSet(viewsets.ModelViewSet):
   queryset = Subject.objects.all()
   serializer_class = SubjectSerializer
   
class TeacherViewSet(viewsets.ModelViewSet):
   queryset = Teacher.objects.all()
   serializer_class = TeacherSerializer

class StudentViewSet(viewsets.ModelViewSet):
   queryset = Student.objects.all()
   serializer_class = StudentSerializer
   
   @action(detail=False, methods=['post'], url_path='upload-image')
   def upload_image(self, request):
      image = request.FILES.get('image')
      if not image:
         return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)

      # Đặt tên file dựa trên tên file gửi lên từ frontend
      filename = image.name  # ví dụ: 123_NguyenVanA_front.jpg

      # Thư mục lưu ảnh (media/student_images/)
      save_path = os.path.join('student_images', filename)
      full_path = os.path.join(settings.MEDIA_ROOT, save_path)

      # Đảm bảo thư mục tồn tại
      os.makedirs(os.path.dirname(full_path), exist_ok=True)

      # Ghi file
      with default_storage.open(save_path, 'wb+') as destination:
         for chunk in image.chunks():
               destination.write(chunk)

      return Response({'message': 'Image saved successfully', 'path': settings.MEDIA_URL + save_path})
   
class ClassViewSet(viewsets.ModelViewSet):
   queryset = Class.objects.all()
   serializer_class = ClassSerializer
   
class RoomViewSet(viewsets.ModelViewSet):
   queryset = Room.objects.all()
   serializer_class = RoomSerializer
   
class ClassTeacherViewSet(viewsets.ModelViewSet):
   queryset = ClassTeacher.objects.all()
   serializer_class = ClassTeacherSerializer
class ClassSubjectViewSet(viewsets.ModelViewSet):
   queryset = ClassSubject.objects.all()
   serializer_class = ClassSubjectSerializer
class ClassRoomViewSet(viewsets.ModelViewSet):
   queryset = ClassRoom.objects.all()
   serializer_class = ClassRoomSerializer
   
   
class TeacherSubjectViewSet(viewsets.ModelViewSet):
   queryset = TeacherSubject.objects.all()
   serializer_class = TeacherSubjectSerializer
class StudentSubjectViewSet(viewsets.ModelViewSet):
   queryset = StudentSubject.objects.all()
   serializer_class = StudentSubjectSerializer
class RoomSubjectViewSet(viewsets.ModelViewSet):
   queryset = RoomSubject.objects.all()
   serializer_class = RoomSubjectSerializer
