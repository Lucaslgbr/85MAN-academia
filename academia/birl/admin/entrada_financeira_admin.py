from academia.utils.admin.generic_admin import GenericAdmin
from django.contrib import admin
from django.urls import reverse_lazy, reverse
from academia.birl.models import EntradaFinanceira, ContaBancaria
from django.utils.html import format_html
from rest_framework.authtoken.models import Token


@admin.register(EntradaFinanceira)
class EntradaFinanceiraAdmin(GenericAdmin):
    list_filter = ['conta_bancaria']
    search_fields = ['id', 'valor', 'data', 'conta_bancaria']
    list_display = ['id','descricao', 'valor', 'data', 'conta_bancaria']
    