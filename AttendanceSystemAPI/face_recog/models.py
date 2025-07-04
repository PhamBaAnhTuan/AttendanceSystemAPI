# face_recog/models.py
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
from subject.models import Class, Subject

class FaceTrainingSession(models.Model):
   student = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='face_training_sessions')
   created_at = models.DateTimeField(auto_now_add=True)
   completed = models.BooleanField(default=False)
   
   def __str__(self):
      return f"Training session for {self.student.name} - {self.created_at}"

class FaceImage(models.Model):
   session = models.ForeignKey(FaceTrainingSession, related_name='images', on_delete=models.CASCADE)
   image = models.ImageField()
   position = models.CharField(max_length=20)  # left, right, front, etc.
   uploaded_at = models.DateTimeField(auto_now_add=True)
   
   def __str__(self):
      return f"Face image for {self.session.student.name} - {self.position}"
    
class AttendanceSession(models.Model):
   session_name = models.CharField(max_length=255)
   start_time = models.DateTimeField(auto_now_add=True)
   end_time = models.DateTimeField(null=True, blank=True)
   is_active = models.BooleanField(default=True)
   
   created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
   classes = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True, related_name='attendance_sessions')
   subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name='attendance_sessions')
   
   def __str__(self):
      return f"{self.session_name} - {self.start_time}"

class Attendance(models.Model):
   session = models.ForeignKey(AttendanceSession, on_delete=models.CASCADE, null=True, blank=True, related_name='attendances')
   student = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
   timestamp = models.DateTimeField(auto_now_add=True)
   confidence = models.FloatField(default=0.0)  # Confidence score of face recognition
   capture_image = models.ImageField(null=True, blank=True)
   
   class Meta:
      unique_together = ('session', 'student')  # Một sinh viên chỉ được điểm danh một lần trong một phiên
   
   def __str__(self):
      return f"{self.student.name} - {self.session.session_name}"