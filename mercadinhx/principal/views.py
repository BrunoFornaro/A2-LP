from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import HttpResponseNotFound, HttpResponseRedirect, Http404
from django.urls import reverse
from principal.models import Produtos, Clientes, Vendas, VendasProdutos
import pandas as pd

import numpy as np
from plotly.io import to_html
import matplotlib.pyplot as plt
import matplotlib as ptl
import plotly.express as px
from plotly.io import to_html



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

    produtos=Produtos().pegar_dados(retornar="dataframe")
    clientes=Clientes().pegar_dados(retornar="dataframe")
    vendas=Vendas().pegar_dados(retornar="dataframe")
    venda_produtos=VendasProdutos().pegar_dados(retornar="dataframe")

    #renomenado a coluna id para id_produto na tabela de produtos
    produtos.rename(columns={"id": "id_produto"}, inplace = 1)
    #realizando a união das tabelas produtos e venda_produtos em id_produtos
    venda_produtos = pd.merge(venda_produtos, produtos, on = 'id_produto', how='right')
    #renomenado a coluna id para id_vendas na tabela de vendas
    vendas.rename(columns={"id": "id_vendas"}, inplace = 1)
    #realizando a união das tabelas vendas e venda_produtos em id_vendas
    venda_produtos = pd.merge(venda_produtos, vendas, on = 'id_vendas', how='right')

    #renomenado a coluna id para id_clientes na tabela de clientes
    clientes.rename(columns={"id": "id_cliente"}, inplace = 1)
    #renomenado a coluna nome para nome_cliente na tabela de clientes
    clientes.rename(columns={"nome": "nome_cliente"}, inplace = 1)

    #realizando a união das tabelas clientes e venda_produtos em id_cliente
    venda_produtos_cliente = pd.merge(venda_produtos, clientes, on = 'id_cliente', how='right')

    #agrupando a tabelas cendas_produto por nome (groupby), somando os valores (sum), organizando os valores em ordem decrescente por quantidade vendida (sort_values) e redefinindo o index (reset_index)
    venda_produtos_total=venda_produtos_cliente.groupby("nome").sum().sort_values('quantidade', ascending=False).reset_index()

    #selecionando apenas as colunas que serão analisadas
    venda_produtos_total[["nome", "quantidade"]]

    #plotagem do gráfico de barras sobre o total de vendas por produto usando plotly
    fig = px.bar(venda_produtos_total,
                x='nome', y="quantidade", height=500, width=700,
                barmode='stack', labels={"nome": "Nome", 'quantidade':"Quantidade vendida"})
    fig.update_layout(title = 'Venda dos produtos')
    fig.update_xaxes(title = 'Produto')
    fig.update_yaxes(title = 'Quantidade vendida')

    figura_barras=to_html(fig, full_html = False)




    context = {"visualizacao1": figura_barras}
    return render(request, "visualizacao1.html",context)

def testes(request):
    context = Produtos().pegar_dados(retornar="dataframe")
    return HttpResponse(f"{context}")