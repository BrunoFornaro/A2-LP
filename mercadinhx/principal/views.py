from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import HttpResponseNotFound, HttpResponseRedirect, Http404
from django.urls import reverse

from principal.models import Produtos, Clientes, Vendas, VendasProdutos

from django.forms.models import model_to_dict

from itertools import chain
def to_dict(instance):
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields):
        data[f.name] = f.value_from_object(instance)
    for f in opts.many_to_many:
        data[f.name] = [i.id for i in f.value_from_object(instance)]
    return data 

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

def produtos(request, id='3'):
    context = Produtos.objects.all()
    context = model_to_dict(context[id])
    return render(request, "produtos.html", context)

def testes(request):
    # Produtos.objects.all().delete()
    # Clientes.objects.all().delete()
    # Vendas.objects.all().delete()
    # VendasProdutos.objects.all().delete()
    resultado = Clientes.objects.all()
    return HttpResponse(f"aaaaaa: {model_to_dict(resultado[11])}")