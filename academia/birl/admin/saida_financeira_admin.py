from academia.utils.admin.generic_admin import GenericAdmin
from django.contrib import admin
from django.urls import reverse_lazy, reverse
from academia.birl.models import SaidaFinanceira
from django.utils.html import format_html

@admin.register(SaidaFinanceira)
class SaidaFinanceiraAdmin(GenericAdmin):
    list_filter = ['conta_bancaria']
    search_fields = ['id', 'valor', 'data', 'conta_bancaria']
    list_display = ['id', 'valor', 'data', 'conta_bancaria']