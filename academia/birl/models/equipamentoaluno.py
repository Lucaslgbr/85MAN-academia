
from django.db import models
from .aluno import Aluno
from .equipamento import Equipamento

class EquipamentoAluno(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    equipamento = models.ForeignKey(Equipamento, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.aluno.nome} - {self.equipamento.nome}"

    class Meta:
        verbose_name = "Equipamento do Aluno"
        verbose_name_plural = "Equipamentos dos Alunos"
