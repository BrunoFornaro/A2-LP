from django.urls import path
from visualizacao3 import views

urlpatterns = [
    path("visualizacao5/", views.visualizacao5, name="visualizacao5")
]