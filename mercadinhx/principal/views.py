from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import HttpResponseNotFound, HttpResponseRedirect, Http404
from django.urls import reverse
from principal.models import Produtos, Clientes, Vendas, VendasProdutos
import pandas as pd

def home(request):
    return render(request, "index.html")

def lista_de_produtos(request):
    produtos = Produtos().pegar_dados()
    context = {"dados": produtos}
    return render(request, "lista_de_produtos_dtl.html", context)

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

def produtos(request, id='3'):
    context = Produtos().pegar_dados()[id]
    return render(request, "produtos.html", context)

def visualizacao1(request):
    context = {"visualizacao1": "visualizacao1"}
    return render(request, "visualizacao1.html",context)

def testes(request):
    context = Produtos().pegar_dados(retornar="dataframe")
    return HttpResponse(f"{context}")