from django.urls import path
from produtos_mais_vendidos import views

urlpatterns = [
    path("visualizacao1/", views.visualizacao1, name="visualizacao1")
]