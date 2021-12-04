from django.urls import path
from visualizacao4 import views

urlpatterns = [
    path("visualizacao4/", views.visualizacao4, name="visualizacao4")
]