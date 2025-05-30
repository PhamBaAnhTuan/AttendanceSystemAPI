class UserFilterBackend:
    def filter_queryset(self, request, queryset, view):
        filters = {}

        role_id = request.query_params.get('role_id')
        faculty_id = request.query_params.get('faculty_id')
        if role_id:
            filters['role_id'] = role_id
        

        queryset = queryset.filter(**filters)
        return queryset