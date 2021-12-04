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

def vendas_por_secao(request):

    # produtos = converter_query(Produtos.objects.all(), retornar="dataframe")
    
    # clientes = converter_query(Clientes.objects.all(), retornar="dataframe")

    # vendas = converter_query(Vendas.objects.all(), retornar="dataframe")
    
    # venda_produtos = converter_query(VendasProdutos.objects.all(), retornar="dataframe")
    # # Selecionando os dados
    # preco = produtos[['id','preco']]
    # # Renomeando a coluna id
    # preco.rename(columns={"id": "id_produto"}, inplace = 1)
    # # Unindo as tabelas venda_produtos e preco
    # venda_preco = pd.merge(venda_produtos, preco, how= 'inner', on= 'id_produto')
    # # Calculando o total arrecadado por produto
    # venda_preco['total_ganho'] = venda_preco['quantidade']*venda_preco['preco']
    # # Agrupando produtos por id
    # venda_preco_prod = venda_preco.groupby('id_produto').sum()
    # # Criando nova variável id para o gráfico
    # venda_preco_prod['id'] = range(len(venda_preco_prod['total_ganho']))
    # # Selecionando dados
    # nome_prod = produtos[['nome', 'id']]
    # # Unindo as tabelas venda_produtos_prod e nome_prod
    # venda_preco_prod = pd.merge(venda_preco_prod, nome_prod, how= 'inner', on= 'id')
    # # Plotando o gráfico
    # fig = px.bar(venda_preco_prod, x='nome', y='total_ganho')
    
    # fig.update_layout(title = 'Receita gerada por cada produto')
    # fig.update_xaxes(title = 'Produto')
    # fig.update_yaxes(title = 'Receita')

    # figura_barras=fig.to_html(full_html=False)

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

    #iniciando gráfico de barras dos clientes que mais gastam
    #adicionando coluna de lucros
    venda_produtos_cliente["lucro"]=(venda_produtos_cliente["preco"]-venda_produtos_cliente["custo"])*venda_produtos_cliente["quantidade"]
    #agrupando os valores por data (para saber lucro total)
    venda_produtos_cliente_soma_lucros = venda_produtos_cliente.groupby("data").sum().sort_values('data').reset_index()

    #separando os valores por seção
    df_acougue=venda_produtos_cliente[venda_produtos_cliente["secao"]=='Açougue']
    df_frutas_e_verduras=venda_produtos_cliente[venda_produtos_cliente["secao"]=='Alimentos em Geral']
    df_padaria=venda_produtos_cliente[venda_produtos_cliente["secao"]=='Padaria']
    df_produtos_de_limpeza=venda_produtos_cliente[venda_produtos_cliente["secao"]=='Produtos de Limpeza']

    #agrupando os valores por data
    df_acougue_lucros = df_acougue.groupby("data").sum().sort_values('data').reset_index()
    df_frutas_e_verduras_lucros = df_frutas_e_verduras.groupby("data").sum().sort_values('data').reset_index()
    df_padaria_lucros = df_padaria.groupby("data").sum().sort_values('data').reset_index()
    df_produtos_de_limpeza_lucros = df_produtos_de_limpeza.groupby("data").sum().sort_values('data').reset_index()

    #iniciando gráfico de linhas do lucro por dia no mes de novembro
    fig_lucro_tempo = go.Figure()
    fig_lucro_tempo.add_trace(go.Scatter(x=venda_produtos_cliente_soma_lucros["data"], y=venda_produtos_cliente_soma_lucros["lucro"], 
                mode = 'markers+lines', name = 'Lucro total'))
    fig_lucro_tempo.add_trace(go.Scatter(x = df_acougue_lucros["data"],
                        y = df_acougue_lucros["lucro"],
                        mode = 'markers+lines',
                        name = 'Lucro por dia no açougue')) 
    fig_lucro_tempo.add_trace(go.Scatter(x = df_frutas_e_verduras_lucros["data"],
                        y = df_frutas_e_verduras_lucros["lucro"],
                        mode = 'markers+lines',
                        name = 'Lucro por dia na seção de alimentos em geral'))
    fig_lucro_tempo.add_trace(go.Scatter(x = df_padaria_lucros["data"],
                        y = df_padaria_lucros["lucro"],
                        mode = 'markers+lines',
                        name = 'Lucro por dia na padaria')) 
    fig_lucro_tempo.add_trace(go.Scatter(x = df_produtos_de_limpeza_lucros["data"],
                        y = df_produtos_de_limpeza_lucros["lucro"],
                        mode = 'markers+lines',
                        name = 'Lucro por dia na seção de limpezas')) 
    fig_lucro_tempo.update_layout(title='Lucro por seção no mês de novembro',
    xaxis_title='Data',
    yaxis_title='Lucro',
    plot_bgcolor = 'white', height=600, width=1200,
    font = {'family': 'Arial','size': 14,'color': 'black'})
    fig_lucro_tempo.update_xaxes( showgrid=True, gridwidth=1, gridcolor='lightgray',
    showline=True, linewidth=1, linecolor='black')
    fig_lucro_tempo.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray',
    showline=True, linewidth=1, linecolor='black')

    # Alterando a cor do fundo
    fig_lucro_tempo.layout.plot_bgcolor = '#F2F2F2'
    fig_lucro_tempo.layout.paper_bgcolor = '#F2F2F2'

    grafico_lucro_tempo=fig_lucro_tempo.to_html(full_html=False, config= {'displayModeBar': False})
    
    #iniciando outro gráfico de lucro por seção
    lucro_secao=venda_produtos_cliente.groupby("secao").sum().sort_values('lucro', ascending=False ).reset_index()

    fig_lucro_secao = px.bar(lucro_secao, x="lucro", y="secao", color="secao", barmode = 'stack', color_discrete_map={'Açougue': '#EF553B', 
                                                   'Padaria': '#AB63FA', 'Produtos de Limpeza': '#FFA15A', 'Alimentos em Geral': '#00CC96'}, 
                labels={"lucro":"Lucro", "secao":"Seção"})
    fig_lucro_secao.update_layout(title = 'Lucros por seção', yaxis={'categoryorder':'total descending'})



    # Alterando a cor do fundo
    fig_lucro_secao.layout.plot_bgcolor = '#F2F2F2'
    fig_lucro_secao.layout.paper_bgcolor = '#F2F2F2'

    grafico_barras_lucro_secao=fig_lucro_secao.to_html(full_html=False, config= {'displayModeBar': False})






    #grafico_lucro_tempo, grafico_barras_lucro_secao

    
    # context = {
    #     "legenda_pergunta":"Você já se perguntou qual é a nossa seção de produtos mais lucrativa?",
    #     "legenda":"Nessa página mostramos as estatísticas de vendas de cada seção dos nossos produtos. Aqui é exibido qual seção foi a mais lucrativa ao decorrer do mês de novembro de 2021",
    #     "link1":"visualizacao2",
    #     "link2":"visualizacao5",
    #     "link3":"visualizacao5",
    #     "botao1":"Produtos mais vendidos",
    #     "botao2":"Vizualização 3",
    #     "botao3":"Vizualização 4",
    #     "grafico": grafico_lucro_tempo + grafico_barras_lucro_secao 
    #     }

    context = {
        "titulo": "Vendas em cada categoria",
        "legenda_pergunta":"Você já se perguntou qual é a nossa categoria de produtos mais lucrativa?",
        "legenda_resposta":"Nessa página mostramos as estatísticas de vendas de cada seção dos nossos produtos. Aqui é exibido qual categoria foi a mais lucrativa ao decorrer do mês de novembro de 2021",
        "botoes": [
            #['nome', 'link']
            ['Produtos mais vendidos','produtos_mais_vendidos'],
            ['Venda por dia da semana','venda_por_dia_da_semana'],
            ['Consumidores mais ativos','consumidores_mais_ativos'],
            ['Relação quantidade e lucro bruto','relacao_quantidade_lucro_bruto']
        ],
        "grafico": grafico_lucro_tempo + grafico_barras_lucro_secao 
        }

    return render(request, "visualizacao1.html",context)
