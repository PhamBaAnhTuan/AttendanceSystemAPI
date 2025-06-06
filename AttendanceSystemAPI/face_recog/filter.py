class SessionFilterBackend:
    def filter_queryset(self, request, queryset, view):
        filters = {}

        date = request.query_params.get('date')
        teacher_id = request.query_params.get('teacher_id')
        class_id = request.query_params.get('class_id')
        subject_id = request.query_params.get('subject_id')
        start_time = request.query_params.get('start_time')
        if date:
            filters['start_time'] = date
        if teacher_id:
            filters['created_by'] = teacher_id
        if class_id:
            filters['classes'] = class_id
        if subject_id:
            filters['subject_id'] = subject_id
        if start_time:
            filters['start_time'] = start_time

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