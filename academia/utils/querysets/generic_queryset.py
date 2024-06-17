from django.db.models import QuerySet


class GenericQueryset(QuerySet):
    
    def get_ids_list(self):
        return self.get_attr_list('id')
    
    def get_attr_list(self, attr, flat=True):
        return self.values_list(attr, flat=flat)