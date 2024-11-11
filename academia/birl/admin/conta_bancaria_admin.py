from academia.utils.admin.generic_admin import GenericAdmin
from django.contrib import admin
from django.urls import reverse_lazy, reverse
from academia.birl.models import ContaBancaria
from django.utils.html import format_html

@admin.register(ContaBancaria)
class ContaBancariaAdmin(GenericAdmin):
    list_filter = []
    search_fields = ['id', 'nome', 'agencia', 'conta']
    list_display = ['id', 'agencia', 'conta', 'nome', 'saldo']