# Importando as bibliotecas necessárias
from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import HttpResponseNotFound, HttpResponseRedirect, Http404
from django.urls import reverse
from principal.models import Produtos
from principal.funcoes import converter_query
from plotly.io import to_html


# View da página principal do site (home)
def home(request):
    # Criando o dicionário com as informações para preencher os cards das seções dos produtos
    context = {
        "secoes": [
            {
                "nome": "Padaria",
                "id": 0,
                "imagem": "padaria.png"
            },
            {
                "nome": "Açougue",
                "id": 1,
                "imagem": "acougue.png"
            },
            {
                "nome": "Alimentos em Geral",
                "id": 2,
                "imagem": "alimentos.png"
            },
            {
                "nome": "Produtos de Limpeza",
                "id": 3,
                "imagem": "produtos_de_limpeza.png"
            }
        ]
    }
    return render(request, "index.html", context)

# View da lista de produtos (ela irá redirecionar para uma view onde a URL vai aparecer melhor apresentada para o usuário)
def lista_de_produtos(request, id='4', filtro="?"):
    # Gera a URL de redirecionamento
    url_redirecionamento = reverse("redirecionada_lista_de_produtos", args=[id,filtro])

    # Redireciona a página (para a mesma página com a URL melhor formatada)
    return HttpResponseRedirect(url_redirecionamento)
    
# View da lista de produtos redirecionada
def redirecionada_lista_de_produtos(request, id='4', filtro="?"):
    # Criando o dicionário com as informações para selecionar as seções
    secoes = {
        "0": ["padaria", "banner_padaria.png"],
        "1": ["acougue", "banner_acougue.png"],
        "2": ["alimentos_em_geral", "alimentos_geral.png"],
        "3": ["produtos_de_limpeza", "produtos_limpeza.png"],
        "4": ["promocoes", "promocao.png"]
    }

    secao = secoes[id]
    # Se a página escolhida for a de promoções, são exibidos todos os produtos de acordo com a ordenação (o padrão retornar em ordem aleatória)
    if secao[0] == "promocoes":
        # Carrega os dados do banco de dados
        produtos = converter_query(Produtos.objects.all().order_by(filtro))
    # Se for escolhida uma seção (que não seja a de promoções) retorna os produtos da seção de acordo com a ordenação (o padrão retornar em ordem aleatória)
    else:
        # Carrega os dados do banco de dados
        produtos = converter_query(Produtos.objects.filter(secao=secao[0]).order_by(filtro))
    
    # Criando o dicionário com as informações para preencher a página dinâmica (alterar as imagens dos banners e filtrar os produtos)
    context = {
        "dados": produtos,
        "banner": secao[1],
        "id": id,
    }

    # Retorna a página dinâmica
    return render(request, "lista_de_produtos_dtl.html", context)


# View de assinatura pró
def assinatura(request):
    # Criando o dicionário com as informações para preencher a página dinâmica (tipos de assinatura)
    context = {"assinaturas":
            [
                {
                "categoria": "Bronze",
                "quantidade_de_pedidos": 1,
                "preco": 10
                },
                {
                    "categoria": "Silver",
                    "quantidade_de_pedidos": 2,
                    "preco": 18
                },
                {
                    "categoria": "Gold",
                    "quantidade_de_pedidos": 4,
                    "preco": 30
                },
                {
                    "categoria": "Platinum",
                    "quantidade_de_pedidos": 10,
                    "preco": 60
                },
                {
                    "categoria": "Diamond",
                    "quantidade_de_pedidos": 20,
                    "preco": 100
                }
            ]
        }

    # Retorna a página de assinatura pró
    return render(request, "assinatura_pro.html", context)

# View da página de cadastro
def cadastro(request):
    # Retorna a página de cadastro
    return render(request, "cadastro.html")

# View para o "fale conosco"
def fale_conosco(request):
    # Retorna a página de "fale conosco"
    return render(request, "fale_conosco.html")

# View para "quem somos"
def quem_somos(request):
    # Retorna a página de quem somos
    return render(request, "quem_somos.html")

# View para a página de recuperação de senha
def recuperar_senha(request):
    # Retorna a página de recuperação de senha
    return render(request, "recuperar_senha.html")

# View para a página de login
def login(request):
    # Retorna a página de login
    return render(request, "login.html")

# View de produtos (ela irá redirecionar para uma view onde a URL vai aparecer melhor apresentada para o usuário)
def produtos(request, id='3'):
    # Gera a URL de redirecionamento
    url_redirecionamento = reverse("redirecionada_produtos", args=[id])

    # Redireciona a página (para a mesma página com a URL melhor formatada)
    return HttpResponseRedirect(url_redirecionamento)
    
# View para a página de produtos redirecionada (com mais informações de um único produto)
def redirecionada_produtos(request, id='4'):
    # Carrega os dados dos produtos do banco de dados
    context = converter_query(Produtos.objects.all())[id]

    # Cria um dicionario com as informações respectivas a cada uma das seções de produtos
    informacoes_secoes = {
        "padaria": f"Nosso produto {context['nome']} é comprado diretamente da fábrica. A produção é feita no município de São Paulo, sem a utilização de agentes químicos que podem ser prejudiciais à saúde, visando o bem estar dos clientes.",
        "acougue": f"Nosso produto {context['nome']} é comprado diretamente do frigorífico. A criação é feita no município de Nova Candelária, sem a utilização de agentes químicos que podem ser prejudiciais à saúde, visando o bem estar dos clientes e animais.",
        "alimentos_em_geral": f"Nosso produto {context['nome']} é comprado diretamente do produtor. A produção é feita no município de Venda Nova do Imigrante, sem a utilização de agrotóxicos ou outros agentes químicos que podem ser nocivos, visando o bem estar dos clientes e bons cuidados com a natureza.",
        "produtos_de_limpeza": f"Nosso produto {context['nome']} é comprado diretamente da fábrica. A produção é feita no município de Rio de Janeiro, sem a utilização de agentes químicos que podem ser nocivos, visando o bem estar dos clientes e bons cuidados com a natureza. Nenhum dos produtos é testado em animais.",
    }

    # Dicionário com todas as informações para preencher a página dinãmica
    context["informacoes"] = informacoes_secoes[context["secao"]]

    # Retorna a página dinâmica
    return render(request, "produtos.html", context)

# # View para testes e para excluir o banco de dados caso necessário
# def testes(request):
#     context = converter_query(Produtos.objects.all())
#     # # Deleta o banco de dados caso necessário (manter comentado quando não for ser usado)
#     # Produtos.objects.all().delete()
#     # Clientes.objects.all().delete()
#     # Vendas.objects.all().delete()
#     # VendasProdutos.objects.all().delete()
#     return HttpResponse(f"{context}")