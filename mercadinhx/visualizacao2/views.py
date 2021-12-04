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
import datetime

def visualizacao2(request):

    produtos = converter_query(Produtos.objects.all(), retornar="dataframe")
    
    clientes = converter_query(Clientes.objects.all(), retornar="dataframe")

    vendas = converter_query(Vendas.objects.all(), retornar="dataframe")
    
    venda_produtos = converter_query(VendasProdutos.objects.all(), retornar="dataframe")
    # Selecionando os dados
    preco = produtos[['id','preco']]
    # Renomeando a coluna id
    preco.rename(columns={"id": "id_produto"}, inplace = 1)
    # Unindo as tabelas venda_produtos e preco
    venda_preco = pd.merge(venda_produtos, preco, how= 'inner', on= 'id_produto')
    # Calculando o total arrecadado por produto
    venda_preco['total_ganho'] = venda_preco['quantidade']*venda_preco['preco']
    # Agrupando produtos por id
    venda_preco_prod = venda_preco.groupby('id_produto').sum()
    # Criando nova variável id para o gráfico
    venda_preco_prod['id'] = range(len(venda_preco_prod['total_ganho']))
    # Selecionando dados
    nome_prod = produtos[['nome', 'id']]
    # Unindo as tabelas venda_produtos_prod e nome_prod
    venda_preco_prod = pd.merge(venda_preco_prod, nome_prod, how= 'inner', on= 'id')
    # Plotando o gráfico
    fig = px.bar(venda_preco_prod, x='nome', y='total_ganho')
    
    fig.update_layout(title = 'Receita gerada por cada produto')
    fig.update_xaxes(title = 'Produto')
    fig.update_yaxes(title = 'Receita')

    figura_barras=fig.to_html(full_html=False)
    
    context = {"visualizacao2": figura_barras}
    return render(request, "visualizacao2.html",context)
    

    