class TeacherFilterBackend:
    def filter_queryset(self, request, queryset, view):
        filters = {}

        teacher_id = request.query_params.get('teacher_id')
        student_id = request.query_params.get('student_id')
        major_id = request.query_params.get('major_id')
        subject_id = request.query_params.get('subject_id')
        class_id = request.query_params.get('class_id')
        role_id = request.query_params.get('role_id')
        faculty_id = request.query_params.get('faculty_id')
        if major_id:
            filters['major_id'] = major_id
        if teacher_id:
            filters['teacher_id'] = teacher_id
        if student_id:
            filters['student_id'] = student_id
        if subject_id:
            filters['subject_id'] = subject_id
        if class_id:
            filters['classes_id'] = class_id
        if role_id:
            filters['role_id'] = role_id
        if faculty_id:
            filters['faculty_id'] = faculty_id

        queryset = queryset.filter(**filters)
        return queryset

class ScheduleFilterBackend:
    def filter_queryset(self, request, queryset, view):
        filters = {}
        date_str = request.query_params.get('date')
        if date_str:
            from datetime import datetime
            try:
                parsed_date = datetime.strptime(date_str, "%d/%m/%Y").date()
                filters['date'] = parsed_date
            except ValueError:
                raise ValidationError({'date': 'Ngày không đúng định dạng dd/mm/yyyy'})
        
        for field in ['classes_id', 'subject_id', 'teacher_id', 'room_id', 'period_id']:
            value = request.query_params.get(field)
            if value:
                filters[f'{field}'] = value
            
        queryset = queryset.filter(**filters)
        return queryset