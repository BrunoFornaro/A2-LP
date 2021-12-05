# Importando as bibliotecas necessárias
from django.urls import path
from venda_por_dia_da_semana import views

# Configurando as URLs da aplicação
urlpatterns = [
    path("", views.venda_por_dia_da_semana, name="venda_por_dia_da_semana")
]