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

# Create your views here.
def visualizacao1(request):

    produtos=Produtos().pegar_dados(retornar="dataframe")
    clientes=Clientes().pegar_dados(retornar="dataframe")
    vendas=Vendas().pegar_dados(retornar="dataframe")
    venda_produtos=VendasProdutos().pegar_dados(retornar="dataframe")

    #renomenado a coluna id para id_produto na tabela de produtos
    produtos.rename(columns={"id": "id_produtos"}, inplace = 1)
    #realizando a união das tabelas produtos e venda_produtos em id_produtos
    venda_produtos = pd.merge(venda_produtos, produtos, on = 'id_produtos', how='right')
    #renomenado a coluna id para id_vendas na tabela de vendas
    vendas.rename(columns={"id": "id_vendas"}, inplace = 1)
    #realizando a união das tabelas vendas e venda_produtos em id_vendas
    venda_produtos = pd.merge(venda_produtos, vendas, on = 'id_vendas', how='right')

    #renomenado a coluna id para id_clientes na tabela de clientes
    clientes.rename(columns={"id": "id_clientes"}, inplace = 1)
    #renomenado a coluna nome para nome_cliente na tabela de clientes
    clientes.rename(columns={"nome": "nome_clientes"}, inplace = 1)

    #realizando a união das tabelas clientes e venda_produtos em id_cliente
    venda_produtos_cliente = pd.merge(venda_produtos, clientes, on = 'id_clientes', how='right')

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

    figura_barras=fig.to_html(full_html=False)




    context = {"visualizacao1": figura_barras}
    return render(request, "visualizacao1.html",context)