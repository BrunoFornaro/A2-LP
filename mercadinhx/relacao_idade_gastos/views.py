# Importando as bibliotecas necessárias
from django.shortcuts import render
from django.http.response import HttpResponseNotFound, HttpResponseRedirect, Http404
from django.urls import reverse
from principal.models import Produtos, Clientes, Vendas, VendasProdutos
from principal.funcoes import converter_query
import pandas as pd
from plotly.subplots import make_subplots
import numpy as np
import plotly.express as px
from plotly.io import to_html
from sklearn.preprocessing import MaxAbsScaler
abs_scaler = MaxAbsScaler()
from datetime import datetime, date


# View para a visualização da análise de relação entre a quantidade vendida e o lucro bruto
def relacao_idade_gastos(request):
    # Carregando os dados
    produtos = converter_query(Produtos.objects.all(), retornar="dataframe")
    # Renomenado a coluna id para id produto na tabela de produtos
    produtos.rename(columns={"id": "id_produtos"}, inplace = 1)

    # Renomeando linhas da coluna secao
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

    # Adicionando tabela de preço total por produto e compra
    venda_produtos_cliente["total_preco"]=venda_produtos_cliente["quantidade"]*venda_produtos_cliente["preco"]
    # Criando nova tabela
    tabela_ajustando_idade=venda_produtos_cliente
    # Transformando a coluna de datas de nascimento como str
    tabela_ajustando_idade["nascimento"]=tabela_ajustando_idade["nascimento"].astype(str)
    # Removendo "-" das linhas na coluna nascimento e substituindo por um espaço
    tabela_ajustando_idade["nascimento"]=tabela_ajustando_idade["nascimento"].str.replace('-',' ')
    # Data de atual
    today = date.today()
    # Função para calcular idade a partir da data de nascimento
    def data(x):
        x=datetime.strptime(x, "%Y %m %d")
        return today.year - x.year - ((today.month, today.day) < (x.month, x.day))
    # Aplicando a função anterior a coluna com as datas de nascimento
    tabela_ajustando_idade["idade"]=tabela_ajustando_idade["nascimento"].apply(lambda x: data(x))
    # Agrupando e somando os dados por nome do cliente
    tabela_ajustando_idade_cliente_gasto=tabela_ajustando_idade[["nome_cliente", "total_preco"]].groupby("nome_cliente").sum().sort_values('total_preco', ascending=False).reset_index()
    # Renomeando coluna "total_preco"
    tabela_ajustando_idade_cliente_gasto.rename(columns={"total_preco": "total_mes"}, inplace = 1)
    # Removendo linhas repetidas
    tabela_ajustando_idade_cliente_idade=tabela_ajustando_idade[["nome_cliente", "idade"]].drop_duplicates()
    # Unindo as tabelas
    tabela_cliente_gasto_idade=pd.merge(tabela_ajustando_idade_cliente_gasto, tabela_ajustando_idade_cliente_idade, on = 'nome_cliente', how='right') 

    #pltagem de um gráfico de disperção relacionado preço e estoque
    fig_gasto_idade=px.scatter(tabela_cliente_gasto_idade, x = "total_mes", y = "idade",hover_data=['nome_cliente'], labels={"total_mes": "Total gasto pelo cliente", "idade": "Idade", "nome_cliente":"Nome do cliente" })
    fig_gasto_idade.update_traces(marker = {'color': '#00CC96'})
    fig_gasto_idade.update_layout(title = 'Gastos totais dos clientes X Idade', font = {'family': 'Arial','size': 14,'color': 'black'})
    fig_gasto_idade.update_xaxes(title = 'Gastos totais dos clientes')
    fig_gasto_idade.update_yaxes(title = 'Idade')


    # Alterando a cor do fundo
    fig_gasto_idade.layout.plot_bgcolor = '#F2F2F2'
    fig_gasto_idade.layout.paper_bgcolor = '#F2F2F2'

    # Exportando o gráfico para html (como string)
    grafico_gasto_idade = fig_gasto_idade.to_html(full_html=False, config={'displayModeBar': False})


    # Criando o dicionário de contexto com as informações para preencher o template (incluindo o gráfico)
    context = {
        "titulo": "Relação entre gastos do cliente e sua idade",
        "legenda_pergunta":"Você já se perguntou se realmente existe relação entre a idade do cliente e seus gastos?",
        "legenda_resposta":"Nessa página mostramos as estatísticas da idade do cliente e seus gastos. Os dados são referentes ao mês de novembro de 2021. Pelo gráfico de dispersão, fica evidente que a idade do consumidor não está relacionada com o quanto ele desembolsa em suas compras.",
        "botoes": [
            #['nome', 'link']
            ['Produtos mais vendidos','produtos_mais_vendidos'],
            ['Lucros por cada categoria','vendas_por_secao'],
            ['Venda por dia da semana','venda_por_dia_da_semana'],
            ['Consumidores mais ativos','consumidores_mais_ativos'],
            ['Relação quantidade e receita bruta','relacao_quantidade_lucro_bruto']
        ],
        "graficos": [grafico_gasto_idade]
        }

    # Retorna a página da visualização (com as informações desejadas)
    return render(request, "visualizacao1.html",context)
