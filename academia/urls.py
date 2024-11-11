"""
URL configuration for academia project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework.reverse import reverse_lazy
from django.contrib.auth.views import *
from academia.birl.views import RelatorioFluxoCaixa

urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('admin:login'))),
    path('admin/', admin.site.urls),
    path('academia/fluxo-caixa/relatorio', login_required(RelatorioFluxoCaixa.as_view()),
        name='relatorio_fluxo_caixa'),
]
