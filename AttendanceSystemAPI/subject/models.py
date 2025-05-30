from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
from django.utils import timezone
import uuid

class Faculty(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    name = models.CharField(max_length=255, unique=True, null=False, blank=False)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
class Major(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name="majors")
    name = models.CharField(max_length=255, unique=True, null=False, blank=False)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
class Subject(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    name = models.CharField(max_length=255, unique=True, null=False, blank=False)
    credit = models.IntegerField(null=False, blank=False, default=3)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name

class Class(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    major = models.ForeignKey(Major, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, unique=True, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name

class Room(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name
    
    # 
class PeriodDefinition(models.Model):
    id = models.AutoField(primary_key=True)
    SHIFT_CHOICES = [
    ('morning', 'Buổi sáng'),
    ('afternoon', 'Buổi chiều'),
    ('evening', 'Buổi tối'),
    ]
    name = models.CharField(max_length=20)  # Ví dụ: "Ca 1"
    shift = models.CharField(max_length=10, choices=SHIFT_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.name} ({self.get_shift_display()}) [{self.start_time} - {self.end_time}]"
class Schedule(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    date = models.DateField(default=timezone.now, null=True, blank=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    classes = models.ForeignKey(Class, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=True)
    period = models.ForeignKey(PeriodDefinition, on_delete=models.CASCADE, null=True, blank=True)
    class Meta:
        unique_together = ['date', 'room', 'period']

    def __str__(self):
        return f"{self.date} - {self.classes} - {self.period.name}"

class TeacherMajor(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="teacher_major")
    major = models.ForeignKey(Major, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    # class Meta:
    #     unique_together = ('teacher', 'major')
class TeacherSubject(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="teacher_subject")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    # class Meta:
    #     unique_together = ('teacher', 'subject')
class TeacherClass(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="teacher_class_name")
    classes = models.ForeignKey(Class, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    # class Meta:
    #     unique_together = ('teacher', 'classes')