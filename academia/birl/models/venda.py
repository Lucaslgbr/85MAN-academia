
from django.db import models
from .entrada_financeira import EntradaFinanceira
from .conta_bancaria import ContaBancaria
from .estoque import Estoque
class Venda(models.Model):
    produto = models.ForeignKey('Produto', on_delete=models.DO_NOTHING)
    quantidade = models.IntegerField()
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    data_venda = models.DateField()

    def __str__(self):
        return f'Venda: {self.quantidade} x {self.produto} : R${self.valor_total}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        print(self.produto)
        if Estoque.objects.filter(produto=self.produto).count() > 0:
            estoque = Estoque.objects.get(produto=self.produto)
            if (estoque.quantidade - self.quantidade) > 0:
                estoque.quantidade = estoque.quantidade - self.quantidade
                estoque.save()
        EntradaFinanceira.objects.create(valor=self.valor_total, descricao=f'Venda {self.produto.descricao}', conta_bancaria=ContaBancaria.objects.first())

    class Meta:
        verbose_name = "Venda"
        verbose_name_plural = "Vendas"
