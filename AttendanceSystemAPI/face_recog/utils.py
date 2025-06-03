
import face_recognition
import numpy as np
import os
from django.conf import settings
import json

def extract_face_encoding(image_path):
   """Extract face encoding from an image"""
   try:
      image = face_recognition.load_image_file(image_path)
      face_locations = face_recognition.face_locations(image)
      
      if not face_locations:
         return None, "No face detected in the image"
      
      # Get encoding of the first face found
      face_encoding = face_recognition.face_encodings(image, [face_locations[0]])[0]
      return face_encoding, None
   except Exception as e:
      return None, str(e)

def process_training_images(images_dict):
   """Process multiple training images and return average encoding
   Skip images where no face is detected"""
   encodings = []
   invalid_images = []
   
   for position, image_path in images_dict.items():
      encoding, error = extract_face_encoding(image_path)
      if encoding is not None:
         encodings.append(encoding)
      else:
         invalid_images.append(f"({position}) {error}")
   
   if not encodings:
      return None, "No valid face encodings could be extracted from any images"
   
   # Calculate average encoding from all processed images
   average_encoding = np.mean(encodings, axis=0)
   
   # If some images failed but we still have at least one valid encoding, return a warning
   warning = None
   if invalid_images:
      warning = f"Processed {len(encodings)} valid images. Skipped images: {', '.join(invalid_images)}"
   
   return average_encoding.tolist(), warning  # Convert to list for JSON serialization

def recognize_faces_in_image(image_path):
   """
   Recognize all faces in an image and return a list of potential matches
   """
   try:
      # Load the image
      image = face_recognition.load_image_file(image_path)
      # Find all faces in the image
      face_locations = face_recognition.face_locations(image)
      
      if not face_locations:
         return [], "No faces detected in the image"
      
      # Get encodings for all faces
      face_encodings = face_recognition.face_encodings(image, face_locations)
      
      # Load all students with face data
      from attendance.models import Student
      students = Student.objects.exclude(face_encodings__isnull=True)
      
      results = []
      
      # Compare each detected face with known student faces
      for face_encoding in face_encodings:
         best_match = None
         best_confidence = 0
         
         for student in students:
               # Get stored encoding
               stored_encoding = student.face_encodings
               
               # Calculate face distance
               face_distance = face_recognition.face_distance([stored_encoding], face_encoding)[0]
               
               # Convert distance to confidence (1 - distance)
               confidence = 1 - face_distance
               
               # Set threshold (e.g., 0.6)
               if confidence > 0.6 and confidence > best_confidence:
                  best_confidence = confidence
                  best_match = student
         
         if best_match:
               results.append({
                  'student_id': best_match.id,
                  'student_name': best_match.name,
                  'confidence': best_confidence
               })
      
      return results, None
      
   except Exception as e:
      return [], str(e)