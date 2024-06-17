
from django.db import models
from .horario import Horario

class Aluno(models.Model):
    nome = models.CharField(max_length=255)
    endereco = models.CharField(max_length=255)
    horario_utilizacao = models.ManyToManyField(Horario)
    frequencia = models.IntegerField()

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Aluno"
        verbose_name_plural = "Alunos"
