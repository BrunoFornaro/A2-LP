from django.urls import path
from produtos_mais_vendidos import views

urlpatterns = [
    path("visualizacao0/", views.visualizacao0, name="visualizacao0")
]