from django.db import models


class AdminPreventRegister(models.Model):
    
    auto_register_admin = False
    
    class Meta:
        abstract = True
