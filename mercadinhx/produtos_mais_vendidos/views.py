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

# Create your views here.
def visualizacao0(request):

    produtos = converter_query(Produtos.objects.all(), retornar="dataframe")
    #renomenado a coluna id para id produto na tabela de produtos
    produtos.rename(columns={"id": "id_produtos"}, inplace = 1)

    clientes = converter_query(Clientes.objects.all(), retornar="dataframe")
    #renomenado a coluna id para id_cliente na tabela de clientes
    clientes.rename(columns={"id": "id_clientes"}, inplace = 1)
    #renomenado a coluna nome para nome_cliente na tabela de clientes
    clientes.rename(columns={"nome": "nome_cliente"}, inplace = 1)

    vendas = converter_query(Vendas.objects.all(), retornar="dataframe")
    #renomenado a coluna id para id_vendas na tabela de vendas
    vendas.rename(columns={"id": "id_vendas"}, inplace = 1)

    venda_produtos = converter_query(VendasProdutos.objects.all(), retornar="dataframe")

    #realizando a união das tabelas produtos e venda_produtos em id_produtos
    venda_produtos_2 = pd.merge(venda_produtos, produtos, on = 'id_produtos', how='inner')
    #realizando a união das tabelas vendas e venda_produtos em id_vendas
    venda_produtos_3 = pd.merge(venda_produtos_2, vendas, on = 'id_vendas', how='inner')
    #realizando a união das tabelas clientes e venda_produtos em id_cliente
    venda_produtos_cliente = pd.merge(venda_produtos_3, clientes, on = 'id_clientes', how='inner')


    #agrupando as tabelas vendas_produto por nome (groupby), somando os valores (sum), organizando os valores em ordem decrescente por quantidade vendida (sort_values) e redefinindo o index (reset_index)
    venda_produtos_total=venda_produtos_cliente.groupby("nome").sum().sort_values('quantidade', ascending=False).reset_index()

    #selecionando apenas as colunas que serão analisadas
    venda_produtos_total[["nome", "quantidade"]]

    #plotagem do gráfico de barras sobre o total de vendas por produto usando plotly
    fig = px.bar(venda_produtos_total,
                x='nome', y="quantidade", 
                barmode='stack', labels={"nome": "Nome", 'quantidade':"Quantidade vendida"})
    fig.update_layout(title = 'Venda dos produtos')
    fig.update_xaxes(title = 'Produto')
    fig.update_yaxes(title = 'Quantidade vendida')
    fig.layout.plot_bgcolor = '#F2F2F2'
    fig.layout.paper_bgcolor = '#F2F2F2'

    figura_barras=fig.to_html(full_html=False)




    context = {"visualizacao1": figura_barras}
    return render(request, "visualizacao1.html",context)