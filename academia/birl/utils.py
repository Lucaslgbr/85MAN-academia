
import weasyprint
from django.template.loader import render_to_string
from django.utils.formats import localize

class Utils:

    @staticmethod
    def build_report(html_template, pdf_context_data, request):
        html = weasyprint.HTML(
            string=render_to_string(html_template, pdf_context_data, request),
            base_url=request.build_absolute_uri())
        return html.write_pdf()

    @staticmethod
    def format_money(value):
        return f'R$ {localize(round(value, 2))}'