from django.urls import path
from consumidores_mais_ativos import views

urlpatterns = [path("", views.consumidores_mais_ativos, name="consumidores_mais_ativos")
]