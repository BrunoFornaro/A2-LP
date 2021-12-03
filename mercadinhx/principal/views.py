from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import HttpResponseNotFound, HttpResponseRedirect, Http404
from django.urls import reverse
from principal.models import Produtos, Clientes, Vendas, VendasProdutos
from django.forms.models import model_to_dict
import pandas as pd

def converter_query(instancia, retornar="lista_de_dicionarios"):
    context = []
    for entrada in instancia:
        entrada = model_to_dict(entrada)
        entrada["id"] = entrada["id"] - 1
        context.append(entrada)
    if retornar == "dataframe":
        context = pd.DataFrame(context)
    return context

def home(request):
    return render(request, "index.html")

def lista_de_produtos(request):
    produtos = Produtos.objects.all()
    context = {"dados": converter_query(produtos)}
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
    context = Produtos.objects.all()
    context = model_to_dict(context[id])
    return render(request, "produtos.html", context)

def teste_uso_template(request):
    produtos = Produtos.objects.all()
    context = {"dados": converter_query(produtos)}
    return render(request, "teste_uso_template.html", context)

def testes(request):
    

    return HttpResponse(f"{context}")
    #return HttpResponse(f"aaaaaa: {model_to_dict(resultado[11])}")