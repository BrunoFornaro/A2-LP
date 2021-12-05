# Importando as bibliotecas necessárias
from django.urls import path
from principal import views 

# Configurando as URLs da aplicação
urlpatterns = [
    # Views da página principal
    path("home/", views.home, name="home"),

    # View dinâmica com informação para a seção dos produtos (id) e a ordenação (filtro) - Com redirecionamento
    # A URL e o nome estão invertido pois um é para o ponto de vista do usuário e outro para o ponto de vista do desenvolvedor
    path("lista_de_produtos_para_redirecionamento/(?P<str:id>\d+)/(?P<str:filtro>\d+)", views.lista_de_produtos, name="lista_de_produtos"),
    path("lista_de_produtos/<str:id>/<str:filtro>", views.redirecionada_lista_de_produtos, name="redirecionada_lista_de_produtos"),

    # View dinâmica para ser atulizada de acordo com o produto escolhido (pelo id) - Com redirecionamento
    path("produtos_para_redirecionamento/(?P<int:id>\d+)", views.produtos, name="produtos"), 
    path("produtos/<int:id>", views.redirecionada_produtos, name="redirecionada_produtos"), 

    # Demais views do site (não dinâmicas e sem redirecionamento)
    path("assinatura/", views.assinatura, name="assinatura"),
    path("cadastro/", views.cadastro, name="cadastro"),
    path("fale_conosco/", views.fale_conosco, name="fale_conosco"), 
    path("quem_somos/", views.quem_somos, name="quem_somos"),
    path("recuperar_senha/", views.recuperar_senha, name="recuperar_senha"),
    path("login/", views.login, name="login"), 
    
    # # View apenas para teste e para excluir os banco de dados caso necessário (deve ser comentada quando não for ser usada)
    # path("testes/", views.testes, name="testes")
]



