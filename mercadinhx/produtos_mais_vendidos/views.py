from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import HttpResponseNotFound, HttpResponseRedirect, Http404
from django.urls import reverse
from principal.models import Produtos, Clientes, Vendas, VendasProdutos
from principal.funcoes import converter_query
import pandas as pd
from plotly.subplots import make_subplots
import numpy as np
from plotly.io import to_html
import matplotlib.pyplot as plt
import matplotlib as ptl
import plotly.express as px
from plotly.io import to_html

# Create your views here.
def visualizacao1(request):

    produtos = converter_query(Produtos.objects.all(), retornar="dataframe")
    #renomenado a coluna id para id produto na tabela de produtos
    produtos.rename(columns={"id": "id_produtos"}, inplace = 1)

    #renomeando linhas da coluna secao
    produtos["secao"].replace({"alimentos_em_geral":"Alimentos em Geral", "acougue": "Açougue", "padaria":"Padaria", "produtos_de_limpeza": "Produtos de Limpeza"}, inplace=True)

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

    #iniciando gráfico de barras das quantidades vendidas por produto
    #agrupando as tabelas vendas_produto por nome (groupby), somando os valores (sum), organizando os valores em ordem decrescente por quantidade vendida (sort_values) e redefinindo o index (reset_index)
    venda_produtos_total=venda_produtos_cliente.groupby("nome").sum().sort_values('quantidade', ascending=False).reset_index()

    #selecionando apenas as colunas que serão analisadas
    venda_produtos_total[["nome", "quantidade"]]

    #plotagem do gráfico de barras sobre o total de vendas por produto usando plotly
    fig_quantidade_produto = px.bar(venda_produtos_total, x='nome', y="quantidade", barmode='stack', labels={"nome": "Nome", 'quantidade':"Quantidade vendida"})
    fig_quantidade_produto.update_layout(title = 'Venda dos produtos')
    fig_quantidade_produto.update_xaxes(title = 'Produto')
    fig_quantidade_produto.update_yaxes(title = 'Quantidade vendida')
    fig_quantidade_produto.update_xaxes(tickangle=45)
    fig_quantidade_produto.show()

    #tranformando gráfico em html
    figura_barras_quantidade_produto=fig_quantidade_produto.to_html(full_html=False)


    #iniciando gráfico de barras da quantidade vendida por secao
    #agrupando os dados por seção
    df_acougue=venda_produtos_cliente[venda_produtos_cliente["secao"]=='Açougue']
    df_frutas_e_verduras=venda_produtos_cliente[venda_produtos_cliente["secao"]=='Alimentos em Geral']
    df_padaria=venda_produtos_cliente[venda_produtos_cliente["secao"]=='Padaria']
    df_produtos_de_limpeza=venda_produtos_cliente[venda_produtos_cliente["secao"]=='Produtos de Limpeza']

    #agrupando os valores por nome do produto em cada tabela das seções
    df_frutas_e_verduras_quantidade=df_frutas_e_verduras.groupby("nome").sum().sort_values('quantidade', ascending=False).reset_index()
    df_acougue_quantidade=df_acougue.groupby("nome").sum().sort_values('quantidade', ascending=False).reset_index()
    df_padaria_quantidade=df_padaria.groupby("nome").sum().sort_values('quantidade', ascending=False).reset_index()
    df_limpeza_quantidade=df_produtos_de_limpeza.groupby("nome").sum().sort_values('quantidade', ascending=False).reset_index()

    #visualização com subplots
    fig_quantidade_secao = make_subplots(rows=2, cols=2, shared_yaxes=True, 
        subplot_titles=("Quantidades vendidas em alimentos em geral", "Quantidades vendidas no açougue", "Quantidades vendidas na padaria", "Quantidades vendidas em produtos de limpeza"))
    #gráficos de barras
    fig_quantidade_secao.add_trace(go.Bar(x=df_frutas_e_verduras_quantidade["nome"], y=df_frutas_e_verduras_quantidade["quantidade"]), 
                1, 1)

    fig_quantidade_secao.add_trace(go.Bar(x=df_acougue_quantidade["nome"], y=df_acougue_quantidade["quantidade"]),
                1, 2)

    fig_quantidade_secao.add_trace(go.Bar(x=df_padaria_quantidade["nome"], y=df_padaria_quantidade["quantidade"]),
                2, 1)

    fig_quantidade_secao.add_trace(go.Bar(x=df_limpeza_quantidade["nome"], y=df_limpeza_quantidade["quantidade"]),
                2, 2)


    fig_quantidade_secao.update_layout(height=650, width=800, showlegend=False,
                    title_text="Produtos mais vendidos")
    fig_quantidade_secao.update_xaxes(tickangle=45)

    #tranformando gráfico em html
    grafico_quantidade_secao=fig_quantidade_secao.to_html(full_html=False)




    #figura_barras_quantidade_produto, grafico_quantidade_secao

    context = {"visualizacao1": figura_barras_quantidade_produto}
    return render(request, "visualizacao1.html",context)