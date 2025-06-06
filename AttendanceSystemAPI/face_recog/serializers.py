# face_recog/serializers.py
from rest_framework import serializers
from .models import FaceTrainingSession, FaceImage, Attendance, AttendanceSession
from django.contrib.auth import get_user_model
User = get_user_model()
from user.serializers import UserInfoShortSerializer
from subject.serializers import ClassShortSerializer, SubjectShortSerializer
from subject.models import Class, Subject, StudentClass

class FaceImageSerializer(serializers.ModelSerializer):
   class Meta:
      model = FaceImage
      fields = ('id', 'image', 'position', 'uploaded_at')
      read_only_fields = ('id', 'uploaded_at')

class FaceTrainingSessionSerializer(serializers.ModelSerializer):
   images = FaceImageSerializer(many=True, read_only=True)
   
   class Meta:
      model = FaceTrainingSession
      fields = ('id', 'student', 'created_at', 'completed', 'images')
      read_only_fields = ('id', 'created_at', 'completed')

class TrainingRequestSerializer(serializers.Serializer):
   image1 = serializers.ImageField(required=True)
   image2 = serializers.ImageField(required=True)
   image3 = serializers.ImageField(required=True)
   image4 = serializers.ImageField(required=True)
   image5 = serializers.ImageField(required=True)

class AttendanceSerializer(serializers.ModelSerializer):
   student_details = UserInfoShortSerializer(source='student', read_only=True)
   
   class Meta:
      model = Attendance
      fields = ['id', 'student_details', 'timestamp', 'confidence']
      # fields = '__all__'
      read_only_fields = ['id', 'timestamp']

class AttendanceSessionSerializer(serializers.ModelSerializer):
   # filter field
   attendances = AttendanceSerializer(many=True, read_only=True)
   attendance_count = serializers.SerializerMethodField()
   
   student = UserInfoShortSerializer(read_only=True)
   classes = ClassShortSerializer(read_only=True)
   subject = SubjectShortSerializer(read_only=True)
   # post field
   teacher_id = serializers.PrimaryKeyRelatedField(
      queryset=User.objects.all(),
      source='created_by',
      required=True,
      write_only=True,
      allow_null=True,
   )
   class_id = serializers.PrimaryKeyRelatedField(
      queryset=Class.objects.all(),
      source='classes',
      required=True,
      write_only=True,
      allow_null=True,
   )
   subject_id = serializers.PrimaryKeyRelatedField(
      queryset=Subject.objects.all(),
      source='subject',
      required=True,
      write_only=True,
      allow_null=True,
   )
   student_count = serializers.SerializerMethodField()

   
   class Meta:
      model = AttendanceSession
      # fields = '__all__'
      fields = ['id', 'session_name', 'start_time', 'end_time', 'is_active', 'created_by', 'student', 'classes', 'subject',
                'teacher_id', 'class_id', 'subject_id', 'attendances', 'attendance_count', 'student_count']
      read_only_fields = ('id', 'start_time', 'end_time', 'is_active')
   
   def get_attendance_count(self, obj):
      return obj.attendances.count()
   def get_student_count(self, obj):
      if not obj.classes:
            return 0
      return StudentClass.objects.filter(classes=obj.classes).count()

    
class VideoAttendanceSerializer(serializers.Serializer):
   video = serializers.FileField(required=True)
   
   def validate_video(self, value):
      # Validate file extension
      allowed_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv']
      file_extension = value.name.split('.')[-1].lower()
      if f'.{file_extension}' not in allowed_extensions:
         raise serializers.ValidationError(
               f"Invalid video format. Allowed formats: {', '.join(allowed_extensions)}"
         )
      
      # Validate file size (max 100MB)
      if value.size > 100 * 1024 * 1024:
         raise serializers.ValidationError("Video file too large. Maximum size is 100MB.")
      
      return value