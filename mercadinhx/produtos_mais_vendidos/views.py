# Importando bibliotecas necessárias
from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import HttpResponseNotFound, HttpResponseRedirect, Http404
from django.urls import reverse
from principal.models import Produtos, Clientes, Vendas, VendasProdutos
from principal.funcoes import converter_query
import pandas as pd
from plotly.subplots import make_subplots
import plotly.express as px
from plotly.io import to_html
import plotly.graph_objects as go

# View para a visualização da análise de produtos mais vendidos
def produtos_mais_vendidos(request):

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

    #iniciando gráfico de barras das quantidades vendidas por produto
    #criando uma tabela apenas com o nome do produto e o preço
    produtos_precos=produtos[["nome", "preco"]]
    #renomenado nome da coluna preco
    produtos_precos.rename(columns={"preco": "preco_unidade"}, inplace = 1)
    #Adicionando coluna de gastos por produto e compra
    venda_produtos_cliente["total_preco"]=venda_produtos_cliente["quantidade"]*venda_produtos_cliente["preco"]
    #agrupando as tabelas venda_produtos_cliente por nome (groupby), somando os valores (sum), organizando os valores em ordem decrescente por quantidade vendida (sort_values) e redefinindo o index (reset_index)
    venda_produtos_total_tudo=venda_produtos_cliente.groupby("nome").sum().sort_values('quantidade', ascending=False).reset_index()
    #selecionando apenas as colunas que serão analisadas
    venda_produtos_total=venda_produtos_total_tudo[["nome", "quantidade"]]
    #Ajustando uma tabela para adicionar seções
    produtos_nome_secao=produtos[["nome", "secao"]].drop_duplicates()
    # Unindo tabelas venda_produtos_total e produtos_nome_secao
    venda_produtos_quantidade_total=pd.merge(produtos_nome_secao, venda_produtos_total, on = 'nome', how='right')
    # Unindo tabelas venda_produtos_quantidade_total e produtos_nome_secao
    venda_produtos_quantidade_total=pd.merge(venda_produtos_quantidade_total, produtos_precos, on = 'nome', how='right')
    # Plotagem do gráfico de barras sobre o total de vendas por produto usando plotly
    fig_quantidade_produto = px.bar(venda_produtos_quantidade_total,
                x='nome', y="quantidade", color="secao", 
                barmode='stack', labels={"nome": "Nome", 'quantidade':"Quantidade vendida", "secao":"Seção"}, color_discrete_map={'Açougue': '#EF553B', 
                                                    'Padaria': '#00CC96', 'Produtos de Limpeza': '#AB63FA', 'Alimentos em Geral': '#636EFA'})
    fig_quantidade_produto.update_layout(title = 'Venda dos produtos', xaxis={'categoryorder':'total descending'}, font = {'family': 'Arial','size': 14,'color': 'black'})
    fig_quantidade_produto.update_xaxes(title = 'Produto')
    fig_quantidade_produto.update_yaxes(title = 'Quantidade vendida')
    fig_quantidade_produto.update_xaxes(tickangle=45)

    # Alterando a cor do fundo
    fig_quantidade_produto.layout.plot_bgcolor = '#F2F2F2'
    fig_quantidade_produto.layout.paper_bgcolor = '#F2F2F2'

    # Exportando o gráfico para html (como string)
    figura_barras_quantidade_produto = fig_quantidade_produto.to_html(full_html=False, config= {'displayModeBar': False})


    # Iniciando gráfico de barras da quantidade vendida por secao
    # Agrupando os dados por seção
    df_acougue=venda_produtos_cliente[venda_produtos_cliente["secao"]=='Açougue']
    df_frutas_e_verduras=venda_produtos_cliente[venda_produtos_cliente["secao"]=='Alimentos em Geral']
    df_padaria=venda_produtos_cliente[venda_produtos_cliente["secao"]=='Padaria']
    df_produtos_de_limpeza=venda_produtos_cliente[venda_produtos_cliente["secao"]=='Produtos de Limpeza']

    # Agrupando os valores por nome do produto em cada tabela das seções
    df_frutas_e_verduras_quantidade=df_frutas_e_verduras.groupby("nome").sum().sort_values('quantidade', ascending=False).reset_index()
    df_acougue_quantidade=df_acougue.groupby("nome").sum().sort_values('quantidade', ascending=False).reset_index()
    df_padaria_quantidade=df_padaria.groupby("nome").sum().sort_values('quantidade', ascending=False).reset_index()
    df_limpeza_quantidade=df_produtos_de_limpeza.groupby("nome").sum().sort_values('quantidade', ascending=False).reset_index()

    # Visualização com subplots
    fig_quantidade_secao = make_subplots(rows=2, cols=2, shared_yaxes=True, 
        subplot_titles=("Quantidades vendidas em alimentos em geral", "Quantidades vendidas no açougue", "Quantidades vendidas na padaria", "Quantidades vendidas em produtos de limpeza"))
    # Gráficos de barras
    fig_quantidade_secao.add_trace(go.Bar(x=df_frutas_e_verduras_quantidade["nome"], y=df_frutas_e_verduras_quantidade["quantidade"], name=""), 
                1, 1)

    fig_quantidade_secao.add_trace(go.Bar(x=df_acougue_quantidade["nome"], y=df_acougue_quantidade["quantidade"], name=""),
                1, 2)

    fig_quantidade_secao.add_trace(go.Bar(x=df_padaria_quantidade["nome"], y=df_padaria_quantidade["quantidade"], name=""),
                2, 1)

    fig_quantidade_secao.add_trace(go.Bar(x=df_limpeza_quantidade["nome"], y=df_limpeza_quantidade["quantidade"], name=""),
                2, 2)


    fig_quantidade_secao.update_layout(showlegend=False,
                    title_text="Produtos mais vendidos por seção", height=700)
    fig_quantidade_secao.update_xaxes(tickangle=45)
    fig_quantidade_secao.update_layout( font = {'family': 'Arial','size': 14,'color': 'black'})

    # Alterando a cor do fundo
    fig_quantidade_secao.layout.plot_bgcolor = '#F2F2F2'
    fig_quantidade_secao.layout.paper_bgcolor = '#F2F2F2'

    #tranformando gráfico em html
    grafico_quantidade_secao = fig_quantidade_secao.to_html(full_html=False, config= {'displayModeBar': False})

    #pltagem de um gráfico de disperção relacionado preço e quantidade
    fig_preco_quantidade=px.scatter(venda_produtos_quantidade_total, x = "quantidade", y = "preco_unidade",  hover_data=['nome'], labels={"preco_unidade": "Preço do produto", "quantidade": "Quantidade vendida", "nome":"Nome do produto" })
    fig_preco_quantidade.update_traces(marker = {'color': '#27430D'})
    fig_preco_quantidade.update_layout(title = 'Relação entre preço do produto e quantidade vendida', font = {'family': 'Arial','size': 14,'color': 'black'})
    fig_preco_quantidade.update_xaxes(title = 'Quantidade vendida')
    fig_preco_quantidade.update_yaxes(title = 'Preço do produto')
    # Alterando a cor do fundo
    fig_preco_quantidade.layout.plot_bgcolor = '#F2F2F2'
    fig_preco_quantidade.layout.paper_bgcolor = '#F2F2F2'
    #tranformando gráfico em html
    grafico_preco_quantidade = fig_preco_quantidade.to_html(full_html=False, config= {'displayModeBar': False})

    # Exportando o gráfico para html (como string)
    grafico_quantidade_secao = fig_quantidade_secao.to_html(full_html=False, config= {'displayModeBar': False})


    # Criando o dicionário de contexto com as informações para preencher o template (incluindo o gráfico)
    context = {
        "titulo": "Produtos mais vendidos",
        "legenda_pergunta":"Você já se perguntou qual é o nosso produto mais vendido?",
        "legenda_resposta":"Nessa página mostramos as estatísticas de vendas dos nossos produtos. Nos gráficos de barras, em ordem decrescente são exibidos quais alimentos foram mais vendidos ao decorrer do mês de novembro de 2021. O morango destaca-se pela ótima qualidade, mesmo tendo uma produção sem agrotóxicos, já a padaria do Mercadinhx faz sucesso com as preparações dos bolos e sanduíches. Além disso, temos um gráfico de dispersão entre o preço do produto e as quantidade vendidas, a partir dele, visualiza-se que há uma correlação muito baixa entre os dados, ou seja, o consumidor não leva em consideração os seus gastos na hora da compra. ",
        "botoes": [
            #['nome', 'link']
            ['Lucros por cada categoria','vendas_por_secao'],
            ['Venda por dia da semana','venda_por_dia_da_semana'],
            ['Consumidores mais ativos','consumidores_mais_ativos'],
            ['Relação quantidade e receita bruta','relacao_quantidade_lucro_bruto'],
            ['Relação idade e gastos do cliente','relacao_idade_gastos']
        ],
        "graficos": [grafico_quantidade_secao, figura_barras_quantidade_produto, grafico_preco_quantidade]
        }

    # Retorna a página da visualização (com as informações desejadas)
    return render(request, "visualizacao1.html", context)