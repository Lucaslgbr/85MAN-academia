from datetime import datetime, timedelta
import weasyprint
from django.contrib import messages
from django.forms import Form, DateField, DateInput, ModelMultipleChoiceField, CheckboxSelectMultiple, ModelChoiceField, ChoiceField
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import TemplateView
from .mixins.admin_context_data_mixin import AdminContextDataMixin
from academia.birl.models import  EntradaFinanceira, SaidaFinanceira
from academia.birl.utils import Utils

class FiltroForm(Form):
    data_inicial = DateField(
        label='Data inicial',
        widget=DateInput(format='%Y-%m-%d', attrs={'type': 'date'})
    )
    data_final = DateField(
        label='Data final',
        widget=DateInput(format='%Y-%m-%d', attrs={'type': 'date'})
    )
    
    
class RelatorioFluxoCaixa(TemplateView, AdminContextDataMixin):
    template_name = 'reports/fluxo_caixa.html'
    form_class = FiltroForm
    model_to_check_permission= EntradaFinanceira


    def get_context_data(self, **kwargs):
        ctx = super(RelatorioFluxoCaixa, self).get_context_data(**kwargs)
        ctx['title'] = 'Relatórios › Relatório de fluxo de caixa'
        ctx['data_inicial'] = data_inicial = self.request.GET.get('data_inicial', '')
        ctx['data_final'] = data_final = self.request.GET.get('data_final', '')

        form = FiltroForm()
        form.fields['data_inicial'].initial = data_inicial if data_inicial else (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        form.fields['data_final'].initial = data_final if data_final else (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        ctx['filter_form'] = form

        entradas = EntradaFinanceira.objects.all()
        saidas = SaidaFinanceira.objects.all()
        if data_inicial and data_final:
            entradas = entradas.filter(data__range=(data_inicial, data_final))
            saidas = saidas.filter(data__range=(data_inicial, data_final))
        print('entradas 1', entradas)
        print('saidas 1', saidas)
        total_entradas = sum(entrada.valor for entrada in entradas)
        total_saidas = sum(saida.valor for saida in saidas)
        ctx['entradas'] = entradas
        ctx['saidas'] = saidas
        ctx['total_entrada'] = Utils.format_money(total_entradas)
        ctx['total_saida'] = Utils.format_money(total_saidas)
        ctx['total_diferenca'] = Utils.format_money(total_entradas - total_saidas)
        return ctx

    def post(self, request, *args, **kwargs):
        ctx = self.get_context_data(**kwargs)
        if not ctx['entradas'] or not ctx['saidas']:
            messages.error(request, 'Não há registros para imprimir')
            return render(request, 'reports/fluxo_caixa_pdf.html', ctx)
        
        if ctx['data_inicial']:
            data_inicial = datetime.strptime(ctx['data_inicial'], '%Y-%m-%d')  
            ctx['data_inicial'] = data_inicial.strftime('%d/%m/%Y') 

        if ctx['data_final']:
            data_final = datetime.strptime(ctx['data_final'], '%Y-%m-%d')  
            ctx['data_final'] = data_final.strftime('%d/%m/%Y') 

        content = weasyprint.HTML(string=render_to_string('reports/fluxo_caixa_pdf.html', {
            'entradas': ctx['entradas'],
            'saidas': ctx['saidas'],
            'total_entrada': ctx['total_entrada'],
            'total_saida': ctx['total_saida'],
            'total_diferenca': ctx['total_diferenca'],
            'data_inicial':  ctx['data_inicial'],
            'data_final': ctx['data_final'],
        }), base_url=self.request.build_absolute_uri())
        pdf = content.write_pdf()
        return HttpResponse(pdf, content_type='application/pdf')