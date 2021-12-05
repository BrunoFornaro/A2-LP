# Importando as bibliotecas necessárias
from django.urls import path
from relacao_quantidade_lucro_bruto import views

# Configurando as URLs da aplicação
urlpatterns = [
    path("", views.relacao_quantidade_lucro_bruto, name="relacao_quantidade_lucro_bruto")
]