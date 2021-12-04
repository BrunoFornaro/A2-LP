from django.urls import path
from relacao_quantidade_lucro_bruto import views

urlpatterns = [
    path("", views.relacao_quantidade_lucro_bruto, name="relacao_quantidade_lucro_bruto")
]