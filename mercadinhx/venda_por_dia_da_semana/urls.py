from django.urls import path
from venda_por_dia_da_semana import views

urlpatterns = [
    path("", views.venda_por_dia_da_semana, name="venda_por_dia_da_semana")
]