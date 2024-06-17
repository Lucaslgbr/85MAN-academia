
from django.db import models

class Venda(models.Model):
    produto = models.CharField(max_length=255)
    quantidade = models.IntegerField()
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    data_venda = models.DateField()

    def __str__(self):
        return self.produto

    class Meta:
        verbose_name = "Venda"
        verbose_name_plural = "Vendas"
