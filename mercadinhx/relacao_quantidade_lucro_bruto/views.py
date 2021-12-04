from django.shortcuts import render
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
from sklearn.preprocessing import MaxAbsScaler
abs_scaler = MaxAbsScaler()


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
    # Agrupando as variáveis por data
    venda_produtos_cliente_agrupado_por_dia=venda_produtos_cliente.groupby("data").sum().sort_values('data')
    # Selecionando dados total_preco e quantidade
    venda_produtos_cliente_agrupado_por_dia=venda_produtos_cliente_agrupado_por_dia[["total_preco", "quantidade"]]

    #Normalizando os dados
    abs_scaler = MaxAbsScaler()
    abs_scaler.fit(venda_produtos_cliente_agrupado_por_dia)
    abs_scaler.max_abs_
    scaled_data = abs_scaler.transform(venda_produtos_cliente_agrupado_por_dia)
    df_scaled = pd.DataFrame(scaled_data, columns=venda_produtos_cliente_agrupado_por_dia.columns)
    df_scaled.transpose()
   
    # Definindo a data com índice
    df_scaled['date'] = np.arange(np.datetime64('2021-11-01'), np.datetime64('2021-12-01'))
    df_scaled = df_scaled.set_index(['date'])
    #renomeando colunas
    df_scaled.rename(columns={'total_preco': 'Renda bruta total', "quantidade": "Quantidade de produtos vendidos"}, inplace = True)

    # Plotando o gráfico
    fig_quantidade_vendida_e_renda = px.line(df_scaled, labels={"variable":"Linhas", "value":"Valor/ Valor Máximo (%)", "date":"Data"}, title="Renda bruta e quantidade vendida no mês de novembro")
    fig_quantidade_vendida_e_renda.update_xaxes(title = 'Data')
    fig_quantidade_vendida_e_renda.update_yaxes(title = 'Valor/ Valor Máximo (%)')
    
    # Alterando a cor do fundo
    fig_quantidade_vendida_e_renda.layout.plot_bgcolor = '#F2F2F2'
    fig_quantidade_vendida_e_renda.layout.paper_bgcolor = '#F2F2F2'

    grafico_quantidade_vendida_e_renda = fig_quantidade_vendida_e_renda.to_html(full_html=False, config={'displayModeBar': False})



    context = {
        "titulo": "venda_por_dia_da_semana",
        "legenda_pergunta":"Pergunta venda_por_dia_da_semana",
        "legenda_resposta":"Texto venda_por_dia_da_semana",
        "botoes": [
            ['produtos_mais_vendidos','produtos_mais_vendidos'],
            ['vendas_por_secao','vendas_por_secao'],
            ['venda_por_dia_da_semana','venda_por_dia_da_semana'],
            ['consumidores_mais_ativos','consumidores_mais_ativos']
        ],
        "grafico": grafico_quantidade_vendida_e_renda
        }


    return render(request, "visualizacao1.html",context)