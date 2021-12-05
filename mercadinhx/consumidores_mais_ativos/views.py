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
import datetime

# Create your views here.

def consumidores_mais_ativos(request):
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
    #adicionado uma coluna dos preços totais pagos por cada cliente em cada produto por compra
    venda_produtos_cliente["total_preco"]=venda_produtos_cliente["quantidade"]*venda_produtos_cliente["preco"]

    #selecionando as colunas desejadas, agrupando a tabela venda_produtos_cliente por id_clientes (groupby), somando os valores (sum), organizando os valores em ordem decrescente por quantidade vendida (sort_values) e redefinindo o index (reset_index)
    quantidade_comprada_preco = venda_produtos_cliente[["id_clientes", "total_preco"]].groupby(['id_clientes']).sum().sort_values('total_preco', ascending=False).reset_index().head(10)
    
    #renomeando coluna total_preco para total_mes
    quantidade_comprada_preco.rename(columns={"total_preco": "total_mes"}, inplace = 1)

    #unindo as tabelas venda_produtos_cliente e quantidade_comprada_preco por id_clientes
    venda_produtos_cliente_pt=pd.merge(venda_produtos_cliente, quantidade_comprada_preco, on = 'id_clientes', how='right') 

    #plotando o gráfico
    fig_total_cliente = px.bar(venda_produtos_cliente_pt, x="nome_cliente", y="total_preco", color="secao", barmode = 'stack', hover_data=['nome', 'data', 'preco'], labels={"total_preco": "Total da compra do produto", "nome_cliente": "Nome do cliente", "nome":"Produto", "data":"Data", "preco":"Preço do produto", "secao":"Seção"})
    fig_total_cliente.update_layout(title = 'Os 10 clientes que mais gastam',
                                    height=700, font = {'family': 'Arial','size': 14,'color': 'black'})

    # Alterando a cor do fundo
    fig_total_cliente.layout.plot_bgcolor = '#F2F2F2'
    fig_total_cliente.layout.paper_bgcolor = '#F2F2F2'

    grafico_total_cliente=fig_total_cliente.to_html(full_html=False, config= {'displayModeBar': False})
    
    #grafico_total_cliente

    # context = {
    #     "legenda_pergunta":"Você já seaaaaaaaaaaaaaaaaaaa perguntou qual é o nosso produto mais vendido?",
    #     "legenda":"Nessa página mostramos aaaaaaaaaaas estatísticas de vendas dos nossos produtos. Em ordem decrescente são exibidos quais alimentos foram mais vendidos ao decorrer do mês de novembro de 2021",
    #     "link1":"visualizacao2",
    #     "link2":"visualizacao5",
    #     "link3":"visualizacao5",
    #     "botao1":"Seção maaaaaais lucrativa",
    #     "botao2":"Vizuaaaaaalização 3",
    #     "botao3":"Vizualização 4",
    #     "grafico": grafico_total_cliente
    #     }

    context = {
        "titulo": "Os 10 clientes mais ativos",
        "legenda_pergunta":"Você já se perguntou quais são os nossos consumidores mais ativos?",
        "legenda_resposta":"Nessa página mostramos as estatísticas do consumo dos nossos clientes mais ativos. Em ordem decrescente são exibidos os clientes mais ativos e os seus respectivos gastos por seção ao decorrer do mês de novembro de 2021. Juliana Viana e Augusto Carvalho são os únicos clientes que despenderam mais de 3 mil reais no mês. Além disso, pelo gráfico, é visível que, em geral, os maiores desembolsos estão relacionados ao açougue, o que se deve ao alto valor das carnes. ",
        "botoes": [
            #['nome', 'link']
            ['Produtos mais vendidos','produtos_mais_vendidos'],
            ['Lucros por cada categoria','vendas_por_secao'],
            ['Venda por dia da semana','venda_por_dia_da_semana'],
            ['Relação quantidade e receita bruta','relacao_quantidade_lucro_bruto']
        ],
        "graficos": [grafico_total_cliente]
        }

    return render(request, "visualizacao1.html",context)
    
    

    