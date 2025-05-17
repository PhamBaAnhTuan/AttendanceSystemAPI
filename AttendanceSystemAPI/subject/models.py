from django.db import models

class User(models.Model):  # Giả sử bạn dùng 1 bảng user chung
    username = models.CharField(max_length=100)
    role = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.username

class Subject(models.Model):
    id = models.IntegerField(primary_key=True, unique=True, null=False, blank=False)
    name = models.CharField(max_length=255)
    credit = models.IntegerField(null=False, blank=False, default=3)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    delete_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
    
class Teacher(models.Model):
    id = models.IntegerField(primary_key=True, unique=True, null=False, blank=False)
    name = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to='images/teacher/', blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    address = models.TextField(blank=True, null=True, default='Da Nang')
    date_of_birth = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    delete_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

class Student(models.Model):
    id = models.IntegerField(primary_key=True, unique=True, null=False, blank=False)
    name = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to='images/student/', blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    address = models.TextField(blank=True, null=True, default='Da Nang')
    date_of_birth = models.DateField(null=True, blank=True, )
    class_id = models.ForeignKey('Class', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    delete_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

class Class(models.Model):
    id = models.CharField(primary_key=True, unique=True, null=False, blank=False)
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    delete_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

class Room(models.Model):
    id = models.IntegerField(primary_key=True, unique=True, null=False, blank=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    delete_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
    

class TeacherSubject(models.Model):
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    delete_at = models.DateTimeField(null=True, blank=True)
class StudentSubject(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    delete_at = models.DateTimeField(null=True, blank=True)
class RoomSubject(models.Model):
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    delete_at = models.DateTimeField(null=True, blank=True)
    
class ClassTeacher(models.Model):
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    delete_at = models.DateTimeField(null=True, blank=True)
class ClassSubject(models.Model):
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    delete_at = models.DateTimeField(null=True, blank=True)
class ClassRoom(models.Model):
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    delete_at = models.DateTimeField(null=True, blank=True)