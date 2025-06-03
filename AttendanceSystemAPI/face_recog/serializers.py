# face_recog/serializers.py
from rest_framework import serializers
from .models import FaceTrainingSession, FaceImage, Attendance, AttendanceSession
from attendance.models import Student
from attendance.serializers import StudentSerializer

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
    student_details = StudentSerializer(source='student', read_only=True)
    
    class Meta:
        model = Attendance
        fields = ('id', 'student', 'student_details', 'timestamp', 'confidence')
        read_only_fields = ('id', 'timestamp')

class AttendanceSessionSerializer(serializers.ModelSerializer):
    attendances = AttendanceSerializer(many=True, read_only=True)
    attendance_count = serializers.SerializerMethodField()
    # created_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = AttendanceSession
        fields = ('id', 'session_name', 'start_time', 'end_time', 'is_active', 'attendances', 'attendance_count')
        read_only_fields = ('id', 'start_time', 'end_time', 'is_active')
    
    def get_attendance_count(self, obj):
        return obj.attendances.count()
    
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