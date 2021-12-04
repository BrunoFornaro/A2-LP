from django.urls import path
from visualizacao1 import views

urlpatterns = [
    path("visualizacao1/", views.visualizacao1, name="visualizacao1")
]