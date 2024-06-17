from django.apps import AppConfig
from django.contrib import admin
from academia.utils.admin.generic_admin import GenericAdmin
class CustomAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name=''
    icon=''
    verbose_name=''

    def ready(self):
        self.register_models()

    def register_auditlog(self,model):
        from auditlog.registry import auditlog
        auditlog_exclude_fields=[]
        if hasattr(model,'auditlog_exclude_fields'):
            auditlog_exclude_fields=getattr(model,'auditlog_exclude_fields')
        if not hasattr(model, 'exclude_from_auditlog'):
            auditlog.register(model,exclude_fields=auditlog_exclude_fields)
    
    def register_admin(self,model):
        if hasattr(model,'auto_register_admin') and not getattr(model,'auto_register_admin'):
            return
        admin.site.register(model,GenericAdmin)

    def register_models(self):
        for model in self.get_models():
            self.register_auditlog(model)        
            self.register_admin(model)