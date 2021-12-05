# Importando as bibliotecas necessárias
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import HttpResponseNotFound, HttpResponseRedirect, Http404
from django.urls import reverse
from principal.models import Produtos, Clientes, Vendas, VendasProdutos
from principal.funcoes import converter_query
import pandas as pd
from plotly.subplots import make_subplots
from plotly.io import to_html
import plotly.express as px

# View para a visualização da análise de venda por dia da semana
def venda_por_dia_da_semana(request):
    # Carregando os dados
    produtos = converter_query(Produtos.objects.all(), retornar="dataframe")
    # Renomenado a coluna id para id produto na tabela de produtos
    produtos.rename(columns={"id": "id_produtos"}, inplace = 1)

    # Renomenado linhas da coluna secao
    produtos["secao"].replace({"alimentos_em_geral":"Alimentos em Geral", "acougue": "Açougue", "padaria":"Padaria", "produtos_de_limpeza": "Produtos de Limpeza"}, inplace=True)

    clientes = converter_query(Clientes.objects.all(), retornar="dataframe")
    # Renomenado a coluna id para id_cliente na tabela de clientes
    clientes.rename(columns={"id": "id_clientes"}, inplace = 1)
    # Renomenado a coluna nome para nome_cliente na tabela de clientes
    clientes.rename(columns={"nome": "nome_cliente"}, inplace = 1)

    vendas = converter_query(Vendas.objects.all(), retornar="dataframe")
    # Renomenado a coluna id para id_vendas na tabela de vendas
    vendas.rename(columns={"id": "id_vendas"}, inplace = 1)

    venda_produtos = converter_query(VendasProdutos.objects.all(), retornar="dataframe")

    # Realizando a união das tabelas produtos e venda_produtos em id_produtos
    venda_produtos_2 = pd.merge(venda_produtos, produtos, on = 'id_produtos', how='inner')
    # Realizando a união das tabelas vendas e venda_produtos em id_vendas
    venda_produtos_3 = pd.merge(venda_produtos_2, vendas, on = 'id_vendas', how='inner')
    # Realizando a união das tabelas clientes e venda_produtos em id_cliente
    venda_produtos_cliente = pd.merge(venda_produtos_3, clientes, on = 'id_clientes', how='inner')

    # Adicionando coluna de preços totais por compra
    venda_produtos_cliente["total_preco"]=venda_produtos_cliente["quantidade"]*venda_produtos_cliente["preco"]
    # Tranformando coluna em tipo data
    venda_produtos_cliente['data'] = pd.to_datetime(venda_produtos_cliente['data'])
    # Adicionando uma coluna com os dias das semanas
    venda_produtos_cliente['dia_sem'] = venda_produtos_cliente['data'].dt.weekday
    # Agrupando os dados por dia da semana, somando, e organizando por ordem crescente de dia
    entrada_bruta_sem = venda_produtos_cliente.groupby(['dia_sem']).sum().sort_values('dia_sem').reset_index()
    # Mudando o nome das linhas da coluna dia_sem
    entrada_bruta_sem["dia_sem"].replace({0:"Segunda-feira", 1: "Terça-feira", 2: "Quarta-feira", 3: "Quinta-feira", 4: "Sexta-feira", 5: "Sábado", 6: "Domingo"}, inplace=True)

    # Plotando Gráfico
    fig_entrada_por_dia = px.bar(entrada_bruta_sem,
                x='dia_sem', y="total_preco",
                labels={"dia_sem": "Dia da semana", "total_preco": "Renda bruta"},
                barmode='stack')
    fig_entrada_por_dia.update_traces(marker = {'color': '#00CC96'})
    fig_entrada_por_dia.update_layout(title = 'Entrada em renda bruta por dia da semana no mês de novembro',
    font = {'family': 'Arial','size': 14,'color': 'black'})
    fig_entrada_por_dia.update_xaxes(title = 'Dia da semana')
    fig_entrada_por_dia.update_yaxes(title = 'Renda bruta')
    
    # Alterando a cor do fundo
    fig_entrada_por_dia.layout.plot_bgcolor = '#F2F2F2'
    fig_entrada_por_dia.layout.paper_bgcolor = '#F2F2F2'

    # Exportando o gráfico para html (como string)
    grafico_entrada_por_dia=fig_entrada_por_dia.to_html(full_html=False, config= {'displayModeBar': False})

    # Criando o dicionário de contexto com as informações para preencher o template (incluindo o gráfico)
    context = {
        "titulo": "Vendas por dia da semana",
        "legenda_pergunta":"Você já se perguntou qual é dia da semana que mais vendemos produtos?",
        "legenda_resposta":"Nessa página mostramos as estatísticas de vendas dos nossos produtos a cada dia da semana. Os dados são referentes ao mês de novembro de 2021",
        "botoes": [
            #['nome', 'link']
            ['Produtos mais vendidos','produtos_mais_vendidos'],
            ['Vendas em cada categoria','vendas_por_secao'],
            ['Consumidores mais ativos','consumidores_mais_ativos'],
            ['Relação quantidade e lucro bruto','relacao_quantidade_lucro_bruto']
        ],
        "graficos": [grafico_entrada_por_dia]
        }
        
    # Retorna a página da visualização (com as informações desejadas)
    return render(request, "visualizacao1.html",context)