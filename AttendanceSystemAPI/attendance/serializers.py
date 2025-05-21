from rest_framework import serializers
from .models import (
    Subject, Teacher, Student, Class, Room,
    ClassTeacher, ClassSubject, ClassRoom,
    TeacherSubject, RoomSubject, StudentSubject
)

class SubjectSerializer(serializers.ModelSerializer):
    # students = serializers.SerializerMethodField()
    # teachers = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
    date_of_birth = serializers.DateField(
        input_formats=['%d/%m/%Y'],
        format='%d/%m/%Y',
    )
    class Meta:
        model = Teacher
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    date_of_birth = serializers.DateField(
        input_formats=['%d/%m/%Y'],
        format='%d/%m/%Y',
    )
    class Meta:
        model = Student
        fields = '__all__'

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'
        
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
        
class ClassSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassSubject
        fields = '__all__'
class ClassTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassTeacher
        fields = '__all__'
class ClassRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoom
        fields = '__all__'
        
class TeacherSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherSubject
        fields = '__all__'
class StudentSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentSubject
        fields = '__all__'
class RoomSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomSubject
        fields = '__all__'

# class TeacherShortSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Teacher
#         fields = 'id'
# class SubjectShortSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Subject
#         fields = ['id', 'name']
# class TeacherSubjectSerializer(serializers.ModelSerializer):
#     teacher_id = serializers.PrimaryKeyRelatedField(
#         queryset=Teacher.objects.all(), write_only=True
#     )
#     teacher_info = TeacherShortSerializer(source='teacher', read_only=True)

#     subject_id = serializers.PrimaryKeyRelatedField(
#         queryset=Subject.objects.all(), write_only=True
#     )
#     subject_info = SubjectShortSerializer(source='subject', read_only=True)
#     class Meta:
#         model = TeacherSubject
#         fields = '__all__'


# class StudentShortSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Student
#         fields = ['id', 'name']
# # class SubjectShortSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = Subject
# #         fields = ['id', 'name']
# class StudentSubjectSerializer(serializers.ModelSerializer):
#     student_id = serializers.PrimaryKeyRelatedField(
#         queryset=Student.objects.all(), write_only=True
#     )
#     student_info = StudentShortSerializer(source='student', read_only=True)

#     subject_id = serializers.PrimaryKeyRelatedField(
#         queryset=Subject.objects.all(), write_only=True
#     )
#     subject_info = SubjectShortSerializer(source='subject', read_only=True)
#     class Meta:
#         model = StudentSubject
#         fields = '__all__'


# class SubjectShortSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Subject
#         fields = ['id', 'name']
# class StudentShortSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Student
#         fields = ['id', 'name']
        
# class ClassSubjectSerializer(serializers.ModelSerializer):
#     # following_user = UserShortSerializer(read_only=True)
#     # followed_user = UserShortSerializer(read_only=True)
#     subject = SubjectShortSerializer(read_only=True)
#     student = StudentShortSerializer(read_only=True)

#     # Cho phép nhận ID khi tạo hoặc update
#     # following_user_id = serializers.PrimaryKeyRelatedField(
#     #     queryset=User.objects.all(), write_only=True, source='following_user'
#     # )
#     # followed_user_id = serializers.PrimaryKeyRelatedField(
#     #     queryset=User.objects.all(), write_only=True, source='followed_user'
#     # )
#     subject_id = serializers.PrimaryKeyRelatedField(
#         queryset=Subject.objects.all(), write_only=True, source='subject'
#     )
#     student_id = serializers.PrimaryKeyRelatedField(
#         queryset=Student.objects.all(), write_only=True, source='student'
#     )
    
#     class Meta:
#         model = ClassSubject
#         fields = '__all__'


# class StudentClassSubSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = StudentClassSub
#         fields = '__all__'
