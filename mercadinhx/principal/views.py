from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import HttpResponseNotFound, HttpResponseRedirect, Http404
from django.urls import reverse
from principal.models import Produtos, Clientes, Vendas, VendasProdutos
from principal.funcoes import converter_query
import pandas as pd

import numpy as np
from plotly.io import to_html
import matplotlib.pyplot as plt
import matplotlib as ptl
import plotly.express as px
from plotly.io import to_html



def home(request):
    return render(request, "index.html")

def lista_de_produtos(request, id='4'):
    secoes = {
        "0": ["padaria", "banner_padaria.png"],
        "1": ["acougue", "banner_acougue.png"],
        "2": ["frutas_e_verduras", "alimentos_geral.png"],
        "3": ["produtos_de_limpeza", "produtos_limpeza.png"],
        "4": ["promocoes", "alimentos_geral.png"]
    }
    secao = secoes[id]
    if secao[0] == "promocoes":
        produtos = converter_query(Produtos.objects.all())
    else:
        produtos = converter_query(Produtos.objects.filter(secao=secao[0]))
    context = {
        "dados": produtos,
        "banner": secao[1]
    }
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
    context = converter_query(Produtos.objects.all())[id]
    return render(request, "produtos.html", context)

def testes(request):
    context = converter_query(Produtos.objects.all())
    # Produtos.objects.all().delete()
    # Clientes.objects.all().delete()
    # Vendas.objects.all().delete()
    # VendasProdutos.objects.all().delete()
    return HttpResponse(f"{context}")