from django.db import models
from django.urls import reverse
from auditlog.registry import auditlog
from django.core.validators import MinValueValidator
from django.db.models import F, Sum
from academia.utils.models.admin_prevent_register import AdminPreventRegister 

class ContaBancaria(AdminPreventRegister):
    agencia = models.CharField(max_length=255)
    conta = models.CharField(max_length=255)
    nome = models.CharField(max_length=255)
    saldo = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = "Conta Bancária"
        verbose_name_plural = "Contas Bancárias"

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse("ContaBancaria_detail", kwargs={"pk": self.pk})
    
    def atualiza_saldo(self):
        entradas = self.entradafinanceira_set.aggregate(soma=Sum('valor'))['soma'] or 0
        saidas = self.saidafinanceira_set.aggregate(soma=Sum('valor'))['soma'] or 0
        saldo_atualizado = entradas - saidas
        self.saldo = saldo_atualizado
        self.save()

auditlog.register(ContaBancaria)