from django.urls import path
from principal import views 

urlpatterns = [
    path("home/", views.home, name="home")
    # path("index/", views.index, name="index"),
    # path("pagina2/", views.pagina2, name="pagina2"),
    # path("pagina3/", views.pagina3, name="pagina3"),
    # path("dinamica/<int:param>", views.dinamica, name="view-dinamica-int"), 
    # path("redireciona/<int:param>", views.redireciona, name="view-redireciona"),
    # path("pagina_dinamica/", views.pagina_dinamica, name="view-pagina-dinamica")  
]