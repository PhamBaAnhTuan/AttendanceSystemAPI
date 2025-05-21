import cv2
import numpy as np
import face_recognition
import os
import pickle
import base64
import logging
from django.conf import settings

# Thiết lập logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def process_base64_image(img_base64):
    """
    Xử lý ảnh base64 và chuyển đổi thành định dạng phù hợp
    """
    if ',' in img_base64:
        img_base64 = img_base64.split(',')[1]
    
    image_data = base64.b64decode(img_base64)
    nparr = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img is None:
        return None, None
    
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img, rgb_img, image_data

def save_training_image(student_id, img_base64, idx):
    """
    Lưu ảnh training vào thư mục
    """
    try:
        img, rgb_img, image_data = process_base64_image(img_base64)
        if img is None:
            return None, "Không thể đọc ảnh"
        
        # Tạo thư mục cho sinh viên
        saved_dir = os.path.join(settings.SAVED_IMAGES_DIR, student_id)
        os.makedirs(saved_dir, exist_ok=True)
        
        # Lưu ảnh vào thư mục
        image_filename = f'image_{idx+1}.jpg'
        image_path = os.path.join(saved_dir, image_filename)
        cv2.imwrite(image_path, img)
        
        return rgb_img, image_data
    except Exception as e:
        logger.error(f"Lỗi khi lưu ảnh: {str(e)}")
        return None, str(e)

def extract_face_encoding(rgb_img):
    """
    Trích xuất face encoding từ ảnh
    """
    try:
        face_locations = face_recognition.face_locations(rgb_img, model="hog")
        
        if len(face_locations) == 0:
            return None, "Không phát hiện khuôn mặt trong ảnh"
        
        face_encodings = face_recognition.face_encodings(rgb_img, face_locations)
        if len(face_encodings) == 0:
            return None, "Không thể trích xuất đặc trưng khuôn mặt"
        
        return face_encodings[0], None
    except Exception as e:
        logger.error(f"Lỗi khi trích xuất face encoding: {str(e)}")
        return None, str(e)

def recognize_faces_in_frame(rgb_img, students_with_encodings):
    """
    Nhận diện các khuôn mặt trong frame dựa vào danh sách encodings
    
    Args:
        rgb_img: Ảnh RGB
        students_with_encodings: Danh sách sinh viên kèm encoding
        
    Returns:
        List các mã sinh viên được nhận diện
    """
    face_locations = face_recognition.face_locations(rgb_img, model="hog")
    
    if not face_locations:
        return []
    
    # Lấy encodings của các khuôn mặt trong frame
    face_encodings = face_recognition.face_encodings(rgb_img, face_locations)
    
    # Danh sách sinh viên được nhận diện
    recognized_students = []
    
    for face_encoding in face_encodings:
        for student in students_with_encodings:
            # Lấy encoding từ pickle binary
            stored_encoding = pickle.loads(student.encoding)
            
            # So sánh khuôn mặt
            matches = face_recognition.compare_faces([stored_encoding], face_encoding, tolerance=0.6)
            
            if matches[0]:
                # Nếu sinh viên chưa được nhận diện trước đó
                if student.student_id not in [s.student_id for s in recognized_students]:
                    recognized_students.append(student)
    
    return recognized_students