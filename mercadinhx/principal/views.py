from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import HttpResponseNotFound, HttpResponseRedirect, Http404
from django.urls import reverse

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

def produtos(request):

    context = {
        "produto":"Morango",
        "preço":"7,99",
        "prateleira":"1A",
        "unidade":"bandeja",
        "quantidade":"50"
    }
    return render(request, "produtos.html", context)
