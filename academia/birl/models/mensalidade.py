
from django.db import models
from .aluno import Aluno
from .entrada_financeira import EntradaFinanceira
from .conta_bancaria import ContaBancaria
class Mensalidade(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField()
    pago = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.aluno.nome} - {self.data_vencimento}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.pago:
            EntradaFinanceira.objects.create(valor=self.valor, descricao=f'Mensalidade {self.aluno.nome}', conta_bancaria=ContaBancaria.objects.first())

    class Meta:
        verbose_name = "Mensalidade"
        verbose_name_plural = "Mensalidades"
