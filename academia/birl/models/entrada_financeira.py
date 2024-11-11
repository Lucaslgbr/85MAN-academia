from django.db import models
from django.core.validators import MinValueValidator
from auditlog.registry import auditlog
from .movimentacao_financeira import MovimentacaoFinanceira


class EntradaFinanceira(MovimentacaoFinanceira):
    pass    

    class Meta:
        verbose_name = "Entrada financeira"
        verbose_name_plural = "Entradas financeiras"

    def __str__(self):
        return f"Entrada - {self.data}"

auditlog.register(EntradaFinanceira)
