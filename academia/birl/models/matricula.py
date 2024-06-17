
from django.db import models
from .aluno import Aluno

class Matricula(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    data_matricula = models.DateField()
    curso = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.aluno.nome} - {self.curso}"

    class Meta:
        verbose_name = "Matrícula"
        verbose_name_plural = "Matrículas"
