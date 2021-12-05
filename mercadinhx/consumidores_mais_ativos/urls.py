# Importando as bibliotecas necessárias
from django.urls import path
from consumidores_mais_ativos import views

# Configurando as URLs da aplicação
urlpatterns = [
    path("", views.consumidores_mais_ativos, name="consumidores_mais_ativos")
]