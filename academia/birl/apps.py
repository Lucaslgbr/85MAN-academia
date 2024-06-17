from django.apps import AppConfig
from academia.utils.apps import CustomAppConfig 

class CoreConfig(CustomAppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'academia.birl'
    icon = 'fa fa-pencil'
    verbose_name = 'Cadastros'
