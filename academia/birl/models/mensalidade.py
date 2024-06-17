
from django.db import models
from .aluno import Aluno

class Mensalidade(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField()
    pago = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.aluno.nome} - {self.data_vencimento}"

    class Meta:
        verbose_name = "Mensalidade"
        verbose_name_plural = "Mensalidades"
