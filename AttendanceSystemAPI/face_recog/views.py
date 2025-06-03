# face_recog/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import FaceTrainingSession, FaceImage, AttendanceSession, Attendance
from .serializers import  AttendanceSessionSerializer, AttendanceSerializer
from .serializers import FaceTrainingSessionSerializer, FaceImageSerializer, TrainingRequestSerializer

from .utils import process_training_images, recognize_faces_in_image
import os
import re
from django.conf import settings
import uuid
from django.db import IntegrityError
from django.utils import timezone

from oauth2_provider.views.mixins import OAuthLibMixin
from AttendanceSystemAPI.views.base import BaseViewSet
from rest_framework.exceptions import NotAuthenticated, PermissionDenied

from django.contrib.auth import get_user_model
User = get_user_model()

class FaceTrainingAPIView(BaseViewSet, OAuthLibMixin):
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
         return FaceTrainingSession.objects.all()
      return FaceTrainingSession.objects.filter(id=user.id)
    
   def extract_student_info_from_filename(self, filename):
      """Extract student ID and position from filename format Student_ID_name_position.png"""
      # pattern = r'{Student}_(\d+)_([^_]+)_(.+)\.(png|jpg|jpeg|bmp|gif|webp)'
      pattern = r'^Student_(\d+)_([^_]+)_(.+)\.(png|jpg|jpeg|bmp|gif|webp)$'
      match = re.match(pattern, filename)
      
      if match:
         student_id = match.group(1)
         student_name = match.group(2)
         position = match.group(3)  # e.g., left, right, front, etc.
         return student_id, student_name, position
      
      return None, None, None
    
   @action(detail=False, methods=['post'])
   def train(self, request):
      """API endpoint to train face recognition with 5 images"""
      serializer = TrainingRequestSerializer(data=request.data)
      
      if not serializer.is_valid():
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
      # Dictionary to group images by student ID
      images_by_student = {}
      
      # Process each uploaded image
      for i in range(1, 6):
         image_key = f'image{i}'
         if image_key in serializer.validated_data:
               image = serializer.validated_data[image_key]
               filename = image.name
               
               # Extract student info from filename
               student_id, student_name, position = self.extract_student_info_from_filename(filename)
               
               if not student_id or not position:
                  return Response({
                     "error": f"Invalid filename format for {filename}. Expected format: Student_ID_name_position.png"
                  }, status=status.HTTP_400_BAD_REQUEST)
               
               # Add to images by student dictionary
               if student_id not in images_by_student:
                  images_by_student[student_id] = {}
               
               images_by_student[student_id][position] = {
                  'image': image,
                  'filename': filename,
                  'student_name': student_name
               }
      
      # Check if we have enough images and they all belong to the same student
      if len(images_by_student) != 1:
         return Response({
               "error": "All images must belong to the same student"
         }, status=status.HTTP_400_BAD_REQUEST)
      
      # Get the student ID and images
      student_id = list(images_by_student.keys())[0]
      student_images = images_by_student[student_id]
      
      # Check if we have at least 5 images
      if len(student_images) < 5:
         return Response({
               "error": f"Need 5 images for training, got {len(student_images)}"
         }, status=status.HTTP_400_BAD_REQUEST)
      
      # Get or create student
      try:
         student = User.objects.get(id=int(student_id))
      except User.DoesNotExist:
         # If student doesn't exist but we have student_name from filename, create a new student
         student_name = list(student_images.values())[0]['student_name']
         student = User.objects.create(
               id=int(student_id),
               name=student_name
         )
      
      # Create training session
      session = FaceTrainingSession.objects.create(student=student)
      
      # Process and save each image
      images_dict = {}
      
      for position, image_data in student_images.items():
         image = image_data['image']
         filename = image_data['filename']
         
         # Save the image with its original name
         image_path = os.path.join(settings.MEDIA_ROOT, 'images/face_training', filename)
         
         # Ensure directory exists
         os.makedirs(os.path.dirname(image_path), exist_ok=True)
         
         # Save image to disk
         with open(image_path, 'wb+') as destination:
               for chunk in image.chunks():
                  destination.write(chunk)
         
         # Create face image record
         face_image = FaceImage.objects.create(
               session=session,
               image=f'images/face_training/{filename}',
               position=position
         )
         
         images_dict[position] = image_path
      
      # Process images to get face encodings
      encodings, message = process_training_images(images_dict)

      if encodings is None:
         session.delete()  # Delete session if training failed completely
         return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)

      # Update student with face encodings
      student.face_encodings = encodings
      student.save()

      # Mark training session as completed
      session.completed = True
      session.save()

      positions_processed = []
      for position in student_images.keys():
         formatted_position = f"Student_{student.id}_{student.name}_{position}"
         positions_processed.append(formatted_position)
      response_data = {
         "message": "Face training completed successfully",
         "student_id": student.id,
         "student_name": student.name,
         "session_id": session.id,
         "positions_processed": positions_processed
      }

      # Add warning message if some images failed
      if message:
         response_data["warning"] = message
      return Response(response_data, status=status.HTTP_201_CREATED)

   @action(detail=False, methods=['get'])
   def status(self, request):
      """Check face training status for a student"""
      student_id = request.query_params.get('student_id')
      
      if not student_id:
         return Response({"error": "student_id parameter is required"}, 
                           status=status.HTTP_400_BAD_REQUEST)
      
      try:
         student = User.objects.get(id=student_id)
         has_face_data = student.face_encodings is not None
         
         last_session = FaceTrainingSession.objects.filter(
               student=student, completed=True
         ).order_by('-created_at').first()
         
         return Response({
               "student_id": student.id,
               "student_name": student.name,
               "has_face_data": has_face_data,
               "last_training": last_session.created_at if last_session else None
         })
         
      except User.DoesNotExist:
         return Response({"error": f"Student with ID {student_id} not found"}, 
                           status=status.HTTP_404_NOT_FOUND)
        
class AttendanceViewSet(viewsets.ModelViewSet):
   queryset = AttendanceSession.objects.all()
   serializer_class = AttendanceSessionSerializer
   # required_alternate_scopes = {
   #    "list": [["admin"], ["teacher"], ["student"]],
   #    "retrieve": [["admin"], ["teacher"], ["student"]],
   #    "create": [["admin"]],
   #    "update": [["admin"]],
   #    "destroy": [["admin"]],
   #    "end_session": [["admin"], ["teacher"]],
   #    "take_attendance": [["admin"], ["teacher"]],
   # }
   def get_queryset(self):
      user = self.request.user
      if not user or not user.is_authenticated:
         raise NotAuthenticated("You must be signin in to access this resource!")
      if not hasattr(user, 'role') or user.role is None:
         raise PermissionDenied("You do not have a role assigned!")
      if user.role.name == "admin":
         return AttendanceSession.objects.all()
      return AttendanceSession.objects.filter(id=user.id)
   
   def create(self, request):
      """Create a new attendance session"""
      serializer = self.get_serializer(data=request.data)
      serializer.is_valid(raise_exception=True)
      
      # Create the session
      session = AttendanceSession.objects.create(
         session_name=serializer.validated_data['session_name'],
         created_by=request.user if request.user.is_authenticated else None,
      )
      
      return Response(self.get_serializer(session).data, status=status.HTTP_201_CREATED)
    
   @action(detail=True, methods=['post'], url_path='end-session')
   def end_session(self, request, pk=None):
      """End an active attendance session"""
      try:
         session = self.get_object()
         
         if not session.is_active:
               return Response({"error": "This session is already ended"}, status=status.HTTP_400_BAD_REQUEST)
         
         session.is_active = False
         session.end_time = timezone.now()
         session.save()
         
         return Response(self.get_serializer(session).data)
         
      except AttendanceSession.DoesNotExist:
         return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)
   
   @action(detail=True, methods=['post'], url_path='take-attendance')
   def take_attendance(self, request, pk=None):
      """Process an image to detect faces and mark attendance"""
      try:
         session = self.get_object()
         
         if not session.is_active:
               return Response({"error": "Cannot take attendance: session is not active"}, 
                              status=status.HTTP_400_BAD_REQUEST)
         
         if 'image' not in request.FILES:
               return Response({"error": "No image provided"}, status=status.HTTP_400_BAD_REQUEST)
         
         uploaded_image = request.FILES['image']
         
         # Save the uploaded image temporarily
         temp_filename = f"attendance_{uuid.uuid4().hex}.png"
         temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')
         os.makedirs(temp_dir, exist_ok=True)
         temp_path = os.path.join(temp_dir, temp_filename)
         
         with open(temp_path, 'wb+') as destination:
               for chunk in uploaded_image.chunks():
                  destination.write(chunk)
         
         try:
               # Process the image to recognize faces
               recognized_faces, error = recognize_faces_in_image(temp_path)
               
               if error and not recognized_faces:
                  return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)
               
               # Track successfully marked attendance
               marked_students = []
               
               # Mark attendance for each recognized face
               for face_data in recognized_faces:
                  try:
                     student = Student.objects.get(id=face_data['student_id'])
                     
                     # Save the image for this attendance record
                     attendance_image_name = f"attendance_{session.id}_{student.id}.png"
                     attendance_image_path = os.path.join(settings.MEDIA_ROOT, 'images/attendance', attendance_image_name)
                     os.makedirs(os.path.dirname(attendance_image_path), exist_ok=True)
                     
                     # Copy the temp image to attendance folder
                     import shutil
                     shutil.copy(temp_path, attendance_image_path)
                     
                     # Create or update attendance record
                     attendance, created = Attendance.objects.update_or_create(
                           session=session,
                           student=student,
                           defaults={
                              'confidence': face_data['confidence'],
                              'capture_image': f'images/attendance/{attendance_image_name}'
                           }
                     )
                     
                     marked_students.append({
                           'student_id': student.id,
                           'student_name': student.name,
                           'confidence': face_data['confidence'],
                           'already_marked': not created,
                           'class_id': student.class_id.id if student.class_id else None,
                     })
                     
                  except Student.DoesNotExist:
                     # Skip if student doesn't exist
                     continue
                  except IntegrityError:
                     # Already marked attendance for this student
                     continue
               
               # Return the results
               return Response({
                  'session_id': session.id,
                  'session_name': session.session_name,
                  'recognized_count': len(recognized_faces),
                  'marked_students': marked_students
               })
               
         finally:
               # Clean up temporary file
               if os.path.exists(temp_path):
                  os.remove(temp_path)
                  
      except AttendanceSession.DoesNotExist:
         return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)
   
   @action(detail=True, methods=['get'], url_path='stats')
   def stats(self, request, pk=None):
      """Get statistics for an attendance session"""
      try:
         session = self.get_object()
         attendances = session.attendances.all()
         
         return Response({
               'session_id': session.id,
               'session_name': session.session_name,
               'start_time': session.start_time,
               'end_time': session.end_time,
               'is_active': session.is_active,
               'total_attendance': attendances.count(),
               'attendances': AttendanceSerializer(attendances, many=True).data
         })
         
      except AttendanceSession.DoesNotExist:
         return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)
      
   @action(detail=True, methods=['post'], url_path='take-attendance-video')
   def take_attendance_video(self, request, pk=None):
      """Process a video to detect faces and mark attendance"""
      try:
         session = self.get_object()
         
         if not session.is_active:
               return Response({"error": "Cannot take attendance: session is not active"}, 
                              status=status.HTTP_400_BAD_REQUEST)
         
         if 'video' not in request.FILES:
               return Response({"error": "No video provided"}, status=status.HTTP_400_BAD_REQUEST)
         
         uploaded_video = request.FILES['video']
         
         # Validate video file
         allowed_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv']
         file_extension = os.path.splitext(uploaded_video.name)[1].lower()
         if file_extension not in allowed_extensions:
               return Response({"error": f"Invalid video format. Allowed: {', '.join(allowed_extensions)}"}, 
                              status=status.HTTP_400_BAD_REQUEST)
         
         # Save the uploaded video temporarily
         temp_filename = f"attendance_video_{uuid.uuid4().hex}{file_extension}"
         temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')
         os.makedirs(temp_dir, exist_ok=True)
         temp_video_path = os.path.join(temp_dir, temp_filename)
         
         with open(temp_video_path, 'wb+') as destination:
               for chunk in uploaded_video.chunks():
                  destination.write(chunk)
         
         try:
               # Process the video to recognize faces
               recognized_faces, error = self.process_video_for_attendance(temp_video_path, session)
               
               if error and not recognized_faces:
                  return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)
               
               # Track successfully marked attendance
               marked_students = []
               
               # Mark attendance for each recognized face
               for face_data in recognized_faces:
                  try:
                     student = Student.objects.get(id=face_data['student_id'])
                     
                     # Create or update attendance record
                     attendance, created = Attendance.objects.update_or_create(
                           session=session,
                           student=student,
                           defaults={
                              'confidence': face_data['confidence'],
                              'capture_image': face_data.get('best_frame_path', None)
                           }
                     )
                     
                     marked_students.append({
                           'student_id': student.id,
                           'student_name': student.name,
                           'class_id': student.class_id.id if student.class_id else None,
                           'confidence': face_data['confidence'],
                           'already_marked': not created,
                           'frame_count': face_data.get('frame_count', 1)
                     })
                     
                  except Student.DoesNotExist:
                     # Skip if student doesn't exist
                     continue
                  except IntegrityError:
                     # Already marked attendance for this student
                     continue
               
               # Return the results
               return Response({
                  'session_id': session.id,
                  'session_name': session.session_name,
                  'video_filename': uploaded_video.name,
                  'total_frames_processed': sum([f.get('frame_count', 1) for f in recognized_faces]),
                  'recognized_count': len(recognized_faces),
                  'marked_students': marked_students
               })
               
         finally:
               # Clean up temporary video file
               if os.path.exists(temp_video_path):
                  os.remove(temp_video_path)
                  
      except AttendanceSession.DoesNotExist:
         return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)
   
   def process_video_for_attendance(self, video_path, session):
      """Process video frames to detect and recognize faces"""
      try:
         import cv2
         import tempfile
         
         # Open video
         cap = cv2.VideoCapture(video_path)
         
         if not cap.isOpened():
               return [], "Could not open video file"
         
         frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
         total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
         
         # Process every nth frame to optimize performance
         frame_skip = max(1, frame_rate // 2)  # Process 2 frames per second
         
         face_detections = {}  # Dictionary to store detections per student
         frame_count = 0
         
         while True:
               ret, frame = cap.read()
               if not ret:
                  break
                  
               frame_count += 1
               
               # Skip frames for performance
               if frame_count % frame_skip != 0:
                  continue
               
               # Save frame temporarily for face recognition
               with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_frame:
                  cv2.imwrite(temp_frame.name, frame)
                  temp_frame_path = temp_frame.name
               
               try:
                  # Recognize faces in this frame
                  frame_results, error = recognize_faces_in_image(temp_frame_path)
                  
                  if frame_results:
                     for face_data in frame_results:
                           student_id = face_data['student_id']
                           confidence = face_data['confidence']
                           
                           if student_id not in face_detections:
                              face_detections[student_id] = {
                                 'student_id': student_id,
                                 'student_name': face_data['student_name'],
                                 'max_confidence': confidence,
                                 'frame_count': 1,
                                 'best_frame_path': None
                              }
                              
                              # Save the best frame for this detection
                              best_frame_filename = f"attendance_{session.id}_{student_id}_video.jpg"
                              best_frame_path = os.path.join(settings.MEDIA_ROOT, 'images/attendance', best_frame_filename)
                              os.makedirs(os.path.dirname(best_frame_path), exist_ok=True)
                              
                              import shutil
                              shutil.copy(temp_frame_path, best_frame_path)
                              face_detections[student_id]['best_frame_path'] = f'images/attendance/{best_frame_filename}'
                           else:
                              face_detections[student_id]['frame_count'] += 1
                              # Update if this frame has higher confidence
                              if confidence > face_detections[student_id]['max_confidence']:
                                 face_detections[student_id]['max_confidence'] = confidence
                                 
                                 # Update best frame
                                 best_frame_filename = f"attendance_{session.id}_{student_id}_video.jpg"
                                 best_frame_path = os.path.join(settings.MEDIA_ROOT, 'images/attendance', best_frame_filename)
                                 
                                 import shutil
                                 shutil.copy(temp_frame_path, best_frame_path)
               
               finally:
                  # Clean up temporary frame
                  if os.path.exists(temp_frame_path):
                     os.remove(temp_frame_path)
         
         cap.release()
         
         # Convert to list format with confidence as max_confidence
         results = []
         for detection in face_detections.values():
               results.append({
                  'student_id': detection['student_id'],
                  'student_name': detection['student_name'],
                  'confidence': detection['max_confidence'],
                  'frame_count': detection['frame_count'],
                  'best_frame_path': detection['best_frame_path']
               })
         
         return results, None
         
      except Exception as e:
         return [], f"Error processing video: {str(e)}"
      