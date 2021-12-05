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


# View para a visualização da análise de relação entre a quantidade vendida e o lucro bruto
def relacao_quantidade_lucro_bruto(request):
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

    # Adicionando coluna de preços totais por compra
    venda_produtos_cliente["total_preco"]=venda_produtos_cliente["quantidade"]*venda_produtos_cliente["preco"]
    # Tranformando coluna em tipo data
    venda_produtos_cliente['data'] = pd.to_datetime(venda_produtos_cliente['data'])
    # Agrupando as variáveis por data
    venda_produtos_cliente_agrupado_por_dia=venda_produtos_cliente.groupby("data").sum().sort_values('data')
    # Selecionando dados total_preco e quantidade
    venda_produtos_cliente_agrupado_por_dia=venda_produtos_cliente_agrupado_por_dia[["total_preco", "quantidade"]]

    # Normalizando os dados
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
    df_scaled.rename(columns={'total_preco': 'Receita bruta total', "quantidade": "Quantidade de produtos vendidos"}, inplace = True)

    # Plotando o gráfico
    fig_quantidade_vendida_e_renda = px.line(df_scaled, labels={"variable":"Linhas", "value":"Valor/ Valor Máximo (%)", "date":"Data"}, title="Receita bruta e quantidade vendida no mês de novembro")
    fig_quantidade_vendida_e_renda.update_layout( font = {'family': 'Arial','size': 14,'color': 'black'})
    fig_quantidade_vendida_e_renda.update_xaxes(title = 'Data')
    fig_quantidade_vendida_e_renda.update_yaxes(title = 'Valor/ Valor Máximo (%)')
    
    # Alterando a cor do fundo
    fig_quantidade_vendida_e_renda.layout.plot_bgcolor = '#F2F2F2'
    fig_quantidade_vendida_e_renda.layout.paper_bgcolor = '#F2F2F2'

    # Exportando o gráfico para html (como string)
    grafico_quantidade_vendida_e_renda = fig_quantidade_vendida_e_renda.to_html(full_html=False, config={'displayModeBar': False})


    # Criando o dicionário de contexto com as informações para preencher o template (incluindo o gráfico)
    context = {
        "titulo": "Relação entre quantidade vendida e receita bruta",
        "legenda_pergunta":"Você já se perguntou se realmente existe relação entre quantidade vendida e receita bruta?",
        "legenda_resposta":"Nessa página mostramos as estatísticas de vendas dos nossos produtos e a receita bruta, demonstrando o quanto os dados são correlacionados. Os dados são referentes ao mês de novembro de 2021.",
        "botoes": [
            #['nome', 'link']
            ['Produtos mais vendidos','produtos_mais_vendidos'],
            ['Lucros por cada categoria','vendas_por_secao'],
            ['Venda por dia da semana','venda_por_dia_da_semana'],
            ['Consumidores mais ativos','consumidores_mais_ativos'],
            ['Relação idade e gastos do cliente','relacao_idade_gastos']
        ],
        "graficos": [grafico_quantidade_vendida_e_renda]
        }

    # Retorna a página da visualização (com as informações desejadas)
    return render(request, "visualizacao1.html",context)