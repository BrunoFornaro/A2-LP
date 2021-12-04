from django.urls import path
from vendas_por_secao import views

urlpatterns = [
    path("", views.vendas_por_secao, name="vendas_por_secao")
]