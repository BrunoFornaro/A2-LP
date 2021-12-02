from django.urls import path
from principal import views 

urlpatterns = [
    path("home/", views.home, name="home"),
    path("lista_de_produtos/", views.lista_de_produtos, name="lista_de_produtos"),
    path("assinatura/", views.assinatura, name="assinatura"),
    path("cadastro/", views.cadastro, name="cadastro"),
    path("fale_conosco/", views.fale_conosco, name="fale_conosco"), 
    path("quem_somos/", views.quem_somos, name="quem_somos"),
    path("recuperar_senha/", views.recuperar_senha, name="recuperar_senha"),
    path("login/", views.login, name="login"), 
    path("produtos/(?P<int:id>\d+)", views.produtos, name="produtos"),
    path("testes/", views.testes, name="testes") ]
