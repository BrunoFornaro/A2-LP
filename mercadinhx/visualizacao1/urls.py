from django.urls import path
from visualizacao1 import views

urlpatterns = [
    path("visualizacao3/", views.visualizacao3, name="visualizacao3")
]