# Importando as bibliotecas necessárias
from django.urls import path
from produtos_mais_vendidos import views

# Configurando as URLs da aplicação
urlpatterns = [
    path("", views.produtos_mais_vendidos, name="produtos_mais_vendidos")
]