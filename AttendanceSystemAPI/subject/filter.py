class TeacherFilterBackend:
    def filter_queryset(self, request, queryset, view):
        filters = {}

        teacher_id = request.query_params.get('teacher_id')
        if teacher_id:
            filters['teacher_id__id'] = teacher_id

        queryset = queryset.filter(**filters)

        # sort_by = request.query_params.get('sortBy')
        # allowed_sort_fields = ['price', '-price']
        # if sort_by in allowed_sort_fields:
        #     order_field = 'product_price' if sort_by == 'price' else '-product_price'
        #     queryset = queryset.order_by(order_field)

        return queryset
