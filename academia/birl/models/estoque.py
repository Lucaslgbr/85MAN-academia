
from django.db import models

class Estoque(models.Model):
    produto = models.CharField(max_length=255)
    quantidade = models.IntegerField()

    def __str__(self):
        return self.produto

    class Meta:
        verbose_name = "Estoque"
        verbose_name_plural = "Estoques"
