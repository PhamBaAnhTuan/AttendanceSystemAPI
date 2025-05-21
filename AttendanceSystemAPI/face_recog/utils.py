import os
import json
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
import face_recognition
from PIL import Image
import io

class FaceEncoder:
    """
    Lớp tiện ích để xử lý và mã hóa khuôn mặt từ ảnh
    """
    
    @staticmethod
    def process_image(image_file) -> Tuple[List[np.ndarray], int]:
        """
        Xử lý ảnh và trích xuất mã hóa khuôn mặt
        
        Args:
            image_file: File ảnh đầu vào (có thể là đường dẫn hoặc file object)
            
        Returns:
            Tuple gồm danh sách các mã hóa khuôn mặt và số lượng khuôn mặt phát hiện được
        """
        # Đọc ảnh
        if isinstance(image_file, str):
            # Nếu là đường dẫn file
            image = face_recognition.load_image_file(image_file)
        else:
            # Nếu là file object (khi upload qua API)
            image_content = image_file.read()
            image = face_recognition.load_image_file(io.BytesIO(image_content))
            
        # Phát hiện vị trí các khuôn mặt trong ảnh
        face_locations = face_recognition.face_locations(image)
        
        # Nếu không phát hiện được khuôn mặt nào
        if len(face_locations) == 0:
            return [], 0
            
        # Mã hóa khuôn mặt
        face_encodings = face_recognition.face_encodings(image, face_locations)
        
        return face_encodings, len(face_locations)
    
    @staticmethod
    def encode_face_from_images(image_files: List[Any]) -> Dict[str, Any]:
        """
        Mã hóa khuôn mặt từ nhiều ảnh và tính toán giá trị trung bình
        
        Args:
            image_files: Danh sách các file ảnh
            
        Returns:
            Dict chứa kết quả mã hóa và thông tin khác
        """
        all_encodings = []
        faces_count = 0
        
        for image_file in image_files:
            encodings, count = FaceEncoder.process_image(image_file)
            if count > 0:
                # Chỉ lấy mã hóa khuôn mặt đầu tiên từ mỗi ảnh
                all_encodings.append(encodings[0])
                faces_count += count
        
        if not all_encodings:
            return {
                "success": False,
                "message": "Không phát hiện được khuôn mặt nào trong các ảnh",
                "faces_detected": 0
            }
            
        # Tính trung bình của các mã hóa
        # Chuyển numpy array thành list để có thể serialize
        avg_encoding = np.mean(all_encodings, axis=0).tolist()
        
        return {
            "success": True,
            "message": f"Đã phát hiện {faces_count} khuôn mặt và tạo mã hóa thành công",
            "faces_detected": faces_count,
            "encoding": avg_encoding
        }
    
    @staticmethod
    def compare_faces(known_encoding: List[float], face_encoding_to_check: List[float], tolerance: float = 0.6) -> bool:
        """
        So sánh hai mã hóa khuôn mặt để xác định có phải cùng một người không
        
        Args:
            known_encoding: Mã hóa khuôn mặt đã biết
            face_encoding_to_check: Mã hóa khuôn mặt cần kiểm tra
            tolerance: Ngưỡng dung sai (mặc định 0.6)
            
        Returns:
            True nếu là cùng một người, False nếu ngược lại
        """
        # Chuyển về numpy array
        known_encoding_np = np.array(known_encoding)
        face_encoding_to_check_np = np.array(face_encoding_to_check)
        
        # Tính khoảng cách Euclid
        face_distance = face_recognition.face_distance([known_encoding_np], face_encoding_to_check_np)[0]
        
        # Kiểm tra nếu khoảng cách nhỏ hơn ngưỡng => cùng một người
        return face_distance <= tolerance
        
    @staticmethod
    def extract_student_info_from_filename(filename: str) -> Dict[str, str]:
        """
        Trích xuất thông tin sinh viên từ tên file
        Format: Student_ID_Tên_[thông tin khác].png
        
        Args:
            filename: Tên file ảnh
            
        Returns:
            Dict chứa student_id và các thông tin khác
        """
        # Loại bỏ phần mở rộng file
        filename_without_ext = os.path.splitext(filename)[0]
        
        # Tách các phần
        parts = filename_without_ext.split('_')
        
        if len(parts) < 3 or parts[0].lower() != 'student':
            return {
                "success": False,
                "message": "Định dạng tên file không hợp lệ. Yêu cầu: Student_ID_Tên_[thông tin khác].png"
            }
            
        return {
            "success": True,
            "student_id": parts[1],
            "student_name": parts[2],
            "extra_info": '_'.join(parts[3:]) if len(parts) > 3 else ""
        }