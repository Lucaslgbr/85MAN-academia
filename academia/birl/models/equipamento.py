
from django.db import models

class Equipamento(models.Model):
    nome = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    localizacao = models.CharField(max_length=255)
    historico_servico = models.TextField()

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Equipamento"
        verbose_name_plural = "Equipamentos"
