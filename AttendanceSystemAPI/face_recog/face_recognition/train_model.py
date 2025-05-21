# attendance/face_recognition/train_model.py
import os
import face_recognition
import numpy as np
import json
from django.conf import settings
from collections import defaultdict

def extract_info_from_filename(filename):
    # Từ Student_01_Phuong.png -> ('01', 'Phuong')
    parts = filename.split('_')
    if len(parts) >= 3:
        student_id = parts[1]
        name = parts[2].split('.')[0]
        return student_id, name
    return None, None

def train_from_images(image_files):
    """
    Train face recognition model từ nhiều ảnh cho mỗi sinh viên
    
    Args:
        image_files: List of uploaded image files
    
    Returns:
        dict: Dictionary với student_id, name, và face_encodings
    """
    # Nhóm ảnh theo student_id
    student_images = defaultdict(list)
    
    for image_file in image_files:
        filename = os.path.basename(image_file.name)
        student_id, name = extract_info_from_filename(filename)
        
        if not student_id or not name:
            continue
        
        student_images[student_id].append({
            'file': image_file,
            'name': name
        })
    
    results = {}
    
    # Xử lý từng sinh viên
    for student_id, images in student_images.items():
        # Lấy tên từ ảnh đầu tiên
        name = images[0]['name']
        face_encodings = []
        
        # Xử lý từng ảnh của sinh viên
        for img_data in images:
            image_file = img_data['file']
            
            # Đọc ảnh và tìm khuôn mặt
            image = face_recognition.load_image_file(image_file)
            face_locations = face_recognition.face_locations(image)
            
            if not face_locations:
                continue  # Không tìm thấy khuôn mặt
            
            # Tạo face encoding
            encoding = face_recognition.face_encodings(image, face_locations)[0]
            face_encodings.append(encoding.tolist())
        
        # Chỉ lưu sinh viên nếu có ít nhất một khuôn mặt được phát hiện
        if face_encodings:
            results[student_id] = {
                'student_id': student_id,
                'name': name,
                'face_encodings': face_encodings,
                'num_images_processed': len(face_encodings)
            }
    
    return results