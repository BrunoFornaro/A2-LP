from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import HttpResponseNotFound, HttpResponseRedirect, Http404
from django.urls import reverse

from principal.models import Produtos

def home(request):
    
    return render(request, "index.html")

def lista_de_produtos(request):
    return render(request, "lista_de_produtos.html")

def assinatura(request):
    return render(request, "assinatura_pro.html")

def cadastro(request):
    return render(request, "cadastro.html")

def fale_conosco(request):
    return render(request, "fale_conosco.html")

def quem_somos(request):
    return render(request, "quem_somos.html")

def recuperar_senha(request):
    return render(request, "recuperar_senha.html")

def login(request):
    return render(request, "login.html")

def teste_uso_template(request):
    return render(request, "teste_uso_template.html")

def produtos(request, id='3'):
    nome_dos_produtos = ["morango", "melancia", "banana", "uva", "batata", "berinjela", "abobrinha", "alface", "couve-flor", "feijão", "arroz", "macarrão"]
    preco_produtos = [7.99, 13.99, 5.99, 7.47, 3.99, 11.99, 3.50, 0.98, 5.48, 8.45, 20.31, 2.48]
    prateleira_dos_produtos = ["1A", "1C", "1B", "1D", "2B", "2D", "2A", "2C", "2E", "3B", "3A", "3C"]
    estoque_produtos = [50, 20, 40, 36, 47, 12, 19, 25, 20, 43, 80, 38]
    unidade_de_medida_estoque = ["bandeja", "unidade", "kg", "bandeja", "kg", "kg", "kg", "pé", "pé", "kg", "kg", "pacote"]
    imagem = ["morango-alt.png", "melancia.jpg", "banana.png", "uva-alt.png", "batata.JPEG", "beringela.jpg", "abobrinha.JPEG", "alface.png", "couve-flor.png", "feijao.png", "arroz.png", "macarrao.jpg"]

    
    nome_do_produto = nome_dos_produtos[id]
    preco_do_produto = preco_produtos[id]
    prateleira_do_produto = prateleira_dos_produtos[id]
    unidade_do_produto = unidade_de_medida_estoque[id]
    quantidade_do_produto = estoque_produtos[id]
    imagem_do_produto = imagem[id]

    context = {
        "produto":nome_do_produto,
        "preço":preco_do_produto,
        "prateleira":prateleira_do_produto,
        "unidade":unidade_do_produto,
        "quantidade":quantidade_do_produto,
        "imagem":imagem_do_produto
    }
    return render(request, "produtos.html", context)

def testes(request):
    resultado = Produtos.objects.all()
    # Produtos.objects.all().delete()
    return HttpResponse(f"aaaaaa: {resultado[11]}")