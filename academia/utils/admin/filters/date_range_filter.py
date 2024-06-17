from typing import Any
from django.contrib.admin import DateFieldListFilter
from django.contrib.admin.options import ModelAdmin
from django.core.handlers.wsgi import WSGIRequest
from django.db.models.base import Model
from django.db.models.fields import Field

class DateRangeFilter(DateFieldListFilter):
    template = 'admin/date_range_filter.html'     

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        self.lookup_kwarg_since = "%s__date__gte" % field_path
        self.lookup_kwarg_until = "%s__date__lte" % field_path