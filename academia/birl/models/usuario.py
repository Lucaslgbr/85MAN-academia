from django.db import models
from django.contrib.auth.models import AbstractUser
from auditlog.registry import auditlog
from academia.utils.models.admin_prevent_register import AdminPreventRegister 

class Usuario(AbstractUser, AdminPreventRegister):
    pass

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return self.first_name
    
auditlog.register(Usuario)
