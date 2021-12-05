# Importando as bibliotecas necessárias
from django.urls import path
from relacao_idade_gastos import views

# Configurando as URLs da aplicação
urlpatterns = [
    path("", views.relacao_idade_gastos, name="relacao_idade_gastos")
]