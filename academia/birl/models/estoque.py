
from django.db import models

class Estoque(models.Model):
    produto = models.ForeignKey('Produto', on_delete=models.DO_NOTHING)
    quantidade = models.IntegerField()

    def __str__(self):
        return f'{self.produto}| Estoque: {self.quantidade}'

    class Meta:
        verbose_name = "Estoque"
        verbose_name_plural = "Estoques"
