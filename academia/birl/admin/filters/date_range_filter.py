from django.contrib.admin import DateFieldListFilter


class DateRangeFilter(DateFieldListFilter):
    template = 'admin/date_range_filter.html'

    def __init__(self, field, request, params, model, model_admin, field_path):
        super(DateRangeFilter, self).__init__(field, request, params, model, model_admin, field_path)
        self.lookup_kwarg_until = '%s__lte' % field_path
