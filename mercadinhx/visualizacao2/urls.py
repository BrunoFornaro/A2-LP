from django.urls import path
from visualizacao2 import views

urlpatterns = [path("visualizacao2/", views.visualizacao2, name="visualizacao2")
]