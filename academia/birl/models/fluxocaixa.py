
from django.db import models

class FluxoCaixa(models.Model):
    descricao = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_movimentacao = models.DateField()

    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name = "Fluxo de Caixa"
        verbose_name_plural = "Fluxo de Caixa"
