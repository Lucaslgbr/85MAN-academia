from django.db import models
from django.core.validators import MinValueValidator
from auditlog.registry import auditlog
from .movimentacao_financeira import MovimentacaoFinanceira


class SaidaFinanceira(MovimentacaoFinanceira):
    pass

    class Meta:
        verbose_name = "Saída financeira"
        verbose_name_plural = "Saídas financeiras"

    def __str__(self):
        return f"Saída - {self.data}"

auditlog.register(SaidaFinanceira)
