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
import plotly.graph_objs as go
import datetime

# Create your views here.
def relacao_quantidade_lucro_bruto(request):
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

    #adicionando coluna de preços totais por compra
    venda_produtos_cliente["total_preco"]=venda_produtos_cliente["quantidade"]*venda_produtos_cliente["preco"]
    #tranformando coluna em tipo data
    venda_produtos_cliente['data'] = pd.to_datetime(venda_produtos_cliente['data'])
    #adicionando uma coluna com os dias das semanas
    venda_produtos_cliente['dia_sem'] = venda_produtos_cliente['data'].dt.weekday
    #agrupando os dados por dia da semana, somando, e organizando por ordem crescente de dia
    entrada_bruta_sem = venda_produtos_cliente.groupby(['dia_sem']).sum().sort_values('dia_sem').reset_index()
    #mudando o nome das linhas da coluna dia_sem
    entrada_bruta_sem["dia_sem"].replace({0:"Segunda-feira", 1: "Terça-feira", 2: "Quarta-feira", 3: "Quinta-feira", 4: "Sexta-feira", 5: "Sábado", 6: "Domingo"}, inplace=True)

    #Plotando Gráfico
    fig_entrada_por_dia = px.bar(entrada_bruta_sem,
                x='dia_sem', y="total_preco",
                labels={"dia_sem": "Dia da semana", "total_preco": "Entrada total"},
                barmode='stack')
    fig_entrada_por_dia.update_layout(title = 'Entrada total por dia da semana no mês de novembro')
    fig_entrada_por_dia.update_xaxes(title = 'Dia da semana')
    fig_entrada_por_dia.update_yaxes(title = 'Entrada')
    

    # Alterando a cor do fundo
    fig_entrada_por_dia.layout.plot_bgcolor = '#F2F2F2'
    fig_entrada_por_dia.layout.paper_bgcolor = '#F2F2F2'

    grafico_entrada_por_dia=fig_entrada_por_dia.to_html(full_html=False, config= {'displayModeBar': False})







    context = {
        "titulo": "relacao_quantidade_lucro_bruto",
        "legenda_pergunta":"Pergunta relacao_quantidade_lucro_bruto",
        "legenda_resposta":"Texto relacao_quantidade_lucro_bruto",
        "botoes": [
            ['produtos_mais_vendidos','produtos_mais_vendidos'],
            ['vendas_por_secao','vendas_por_secao'],
            ['venda_por_dia_da_semana','venda_por_dia_da_semana'],
            ['consumidores_mais_ativos','consumidores_mais_ativos']
        ],
        "grafico": grafico_entrada_por_dia
        }
        
    return render(request, "visualizacao1.html",context)