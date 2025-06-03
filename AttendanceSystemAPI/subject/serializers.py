from rest_framework import serializers
from user.models import User
from .models import (
   Faculty, Major,
   Subject, Class, Room,
   TeacherMajor, TeacherClass, TeacherSubject, TeacherClassSubject,
   StudentClass,
   Schedule, PeriodDefinition,
)
from user.models import User
from roles.serializer import RoleSerializer
from user.serializers import UserInfoSerializer


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ['id', 'name']

class MajorSerializer(serializers.ModelSerializer):
    # get field
    faculty = FacultySerializer(read_only=True)
    # post field
    faculty_id = serializers.PrimaryKeyRelatedField(
        queryset=Faculty.objects.all(),
        source='faculty',
        required=True,
        write_only=True,
        allow_null=True,
    )
    class Meta:
        model = Major
        fields = ['id', 'name', 'faculty', 'faculty_id']
class MajorShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Major
        fields = ['id', 'name']

class SubjectSerializer(serializers.ModelSerializer):
    # get field
    major = MajorSerializer(read_only=True)
    # post field
    major_id = serializers.PrimaryKeyRelatedField(
        queryset=Major.objects.all(),
        source='major',
        required=True,
        write_only=True,
        allow_null=True,
    )
    class Meta:
        model = Subject
        fields = ['id', 'name', 'major', 'major_id', 'credit', 'description']
class SubjectShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name']
        
class ClassSerializer(serializers.ModelSerializer):
    # get field
    major = MajorSerializer(read_only=True)
    # post field
    major_id = serializers.PrimaryKeyRelatedField(
        queryset=Major.objects.all(),
        source='major',
        required=True,
        write_only=True,
        allow_null=True,
    )
    class Meta:
        model = Class
        fields = ['id', 'name', 'major', 'major_id']
class ClassShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['id', 'name']
        
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
class RoomShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name']
        
class TeacherShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']
class TeacherMajorSerializer(serializers.ModelSerializer):
    # filter field
    teacher = TeacherShortSerializer(read_only=True)
    major = MajorShortSerializer(read_only=True)
    # post field
    teacher_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='teacher',
        required=True,
        write_only=True,
        allow_null=True,
    )
    major_id = serializers.PrimaryKeyRelatedField(
        queryset=Major.objects.all(),
        source='major',
        required=True,
        write_only=True,
        allow_null=True,
    )
    class Meta:
        model = TeacherMajor
        fields = ['id', 'teacher_id', 'major_id', 'teacher', 'major']
    
    def validate(self, attrs):
        teacher = attrs.get('teacher')
        major = attrs.get('major')

        if TeacherMajor.objects.filter(teacher=teacher, major=major).exists():
            raise serializers.ValidationError("This teacher is already assigned to this major.")

        return attrs
class TeacherClassSerializer(serializers.ModelSerializer):
    # filter field
    teacher = TeacherShortSerializer(read_only=True)
    classes = ClassShortSerializer(read_only=True)
    # post field
    teacher_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='teacher',
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
    class Meta:
        model = TeacherClass
        fields = ['id', 'teacher_id', 'class_id', 'teacher', 'classes']
    
    def validate(self, attrs):
        teacher = attrs.get('teacher')
        classes = attrs.get('classes')

        if TeacherClass.objects.filter(teacher=teacher, classes=classes).exists():
            raise serializers.ValidationError("This teacher is already assigned to this class.")

        return attrs
# 
class StudentClassSerializer(serializers.ModelSerializer):
    # filter field
    student = TeacherShortSerializer(read_only=True)
    classes = ClassShortSerializer(read_only=True)
    # post field
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='student',
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
    class Meta:
        model = StudentClass
        fields = ['id', 'student_id', 'class_id', 'student', 'classes']
    
    def validate(self, attrs):
        student = attrs.get('student')
        classes = attrs.get('classes')

        if StudentClass.objects.filter(student=student, classes=classes).exists():
            raise serializers.ValidationError("This student is already assigned to this class.")

        return attrs

class TeacherSubjectSerializer(serializers.ModelSerializer):
    # filter field
    teacher = TeacherShortSerializer(read_only=True)
    subject = SubjectShortSerializer(read_only=True)
    # post field
    teacher_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='teacher',
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
    class Meta:
        model = TeacherSubject
        fields = ['id', 'teacher_id', 'subject_id', 'teacher', 'subject']
    
    def validate(self, attrs):
        teacher = attrs.get('teacher')
        subject = attrs.get('subject')

        if TeacherSubject.objects.filter(teacher=teacher, subject=subject).exists():
            raise serializers.ValidationError("This teacher is already assigned to this subject.")

        return attrs
    
class TeacherClassSubjectSerializer(serializers.ModelSerializer):
    # filter field
    teacher = TeacherShortSerializer(read_only=True)
    classes = ClassShortSerializer(read_only=True)
    subject = SubjectShortSerializer(read_only=True)
    # post field
    teacher_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='teacher',
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
    class Meta:
        model = TeacherClassSubject
        fields = ['id', 'teacher_id', 'class_id', 'subject_id', 'teacher', 'classes', 'subject']
    
    def validate(self, attrs):
        teacher = attrs.get('teacher')
        classes = attrs.get('classes')
        subject = attrs.get('subject')

        if TeacherClassSubject.objects.filter(teacher=teacher, classes=classes, subject=subject).exists():
            raise serializers.ValidationError("This teacher is already assigned to this subject in this class.")

        return attrs
        
class PeriodDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodDefinition
        fields = ['id', 'name', 'shift', 'start_time', 'end_time']

class ScheduleSerializer(serializers.ModelSerializer):
    date = serializers.DateField(
        input_formats=['%d/%m/%Y'],
        format='%d/%m/%Y',
    )
    # get field
    teacher = TeacherShortSerializer(read_only=True)
    period = PeriodDefinitionSerializer(read_only=True)
    subject = SubjectShortSerializer(read_only=True)
    classes = ClassShortSerializer(read_only=True)
    room = RoomShortSerializer(read_only=True)
    # post field
    teacher_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='teacher',
        required=True,
        write_only=True,
        allow_null=True,
    )
    period_id = serializers.PrimaryKeyRelatedField(
        queryset=PeriodDefinition.objects.all(),
        source='period',
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
    room_id = serializers.PrimaryKeyRelatedField(
        queryset=Room.objects.all(),
        source='room',
        write_only=True,
        required=True,
    )
    class_id = serializers.PrimaryKeyRelatedField(
        queryset=Class.objects.all(),
        source='classes',
        write_only=True,
        required=True,
    )
    
    class Meta:
        model = Schedule
        fields = '__all__'