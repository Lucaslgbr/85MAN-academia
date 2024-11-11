from django.db import models
from django.core.validators import MinValueValidator
from auditlog.registry import auditlog
from django.core.validators import MinValueValidator
from academia.utils.models.admin_prevent_register import AdminPreventRegister 

class MovimentacaoFinanceira(AdminPreventRegister):
    valor = models.DecimalField(default=0, max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    data = models.DateTimeField(auto_now_add=True)
    descricao = models.CharField(max_length=255)
    conta_bancaria = models.ForeignKey('ContaBancaria', on_delete=models.DO_NOTHING)
    
    class Meta:
        abstract = True

    def __str__(self):
        return f"Movimentação - {self.data}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.conta_bancaria.atualiza_saldo()  

auditlog.register(MovimentacaoFinanceira)

