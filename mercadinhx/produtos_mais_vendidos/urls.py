from django.urls import path
from produtos_mais_vendidos import views

urlpatterns = [
    path("", views.produtos_mais_vendidos, name="produtos_mais_vendidos")
]