
from django.db import models
from .aluno import Aluno

class Frequencia(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    data = models.DateField()
    presente = models.BooleanField()

    def __str__(self):
        return f"{self.aluno.nome} - {self.data}"

    class Meta:
        verbose_name = "Frequência"
        verbose_name_plural = "Frequências"
