# Importando as bibliotecas necessárias
from django.urls import path
from vendas_por_secao import views

# Configurando as URLs da aplicação
urlpatterns = [
    path("", views.vendas_por_secao, name="vendas_por_secao")
]