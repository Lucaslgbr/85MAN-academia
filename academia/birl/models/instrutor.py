
from django.db import models
from .horario import Horario

class Instrutor(models.Model):
    nome = models.CharField(max_length=255)
    qualificacoes = models.TextField()
    horarios = models.ManyToManyField(Horario)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Instrutor"
        verbose_name_plural = "Instrutores"
