# Importando as bibliotecas necessárias
from django.http import response
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
import plotly.graph_objs as go

# View para a visualização da análise das vendas por seção
def vendas_por_secao(request):
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

    # Iniciando gráfico de barras dos clientes que mais gastam
    #adicionando coluna de lucros
    venda_produtos_cliente["lucro"]=(venda_produtos_cliente["preco"]-venda_produtos_cliente["custo"])*venda_produtos_cliente["quantidade"]
    # Aagrupando os valores por data (para saber lucro total)
    venda_produtos_cliente_soma_lucros = venda_produtos_cliente.groupby("data").sum().sort_values('data').reset_index()

    # Separando os valores por seção
    df_acougue=venda_produtos_cliente[venda_produtos_cliente["secao"]=='Açougue']
    df_frutas_e_verduras=venda_produtos_cliente[venda_produtos_cliente["secao"]=='Alimentos em Geral']
    df_padaria=venda_produtos_cliente[venda_produtos_cliente["secao"]=='Padaria']
    df_produtos_de_limpeza=venda_produtos_cliente[venda_produtos_cliente["secao"]=='Produtos de Limpeza']

    # Agrupando os valores por data
    df_acougue_lucros = df_acougue.groupby("data").sum().sort_values('data').reset_index()
    df_frutas_e_verduras_lucros = df_frutas_e_verduras.groupby("data").sum().sort_values('data').reset_index()
    df_padaria_lucros = df_padaria.groupby("data").sum().sort_values('data').reset_index()
    df_produtos_de_limpeza_lucros = df_produtos_de_limpeza.groupby("data").sum().sort_values('data').reset_index()

    # Iniciando gráfico de linhas do lucro por dia no mes de novembro
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
    plot_bgcolor = 'white',
    font = {'family': 'Arial','size': 14,'color': 'black'})
    fig_lucro_tempo.update_xaxes( showgrid=True, gridwidth=1, gridcolor='lightgray',
    showline=True, linewidth=1, linecolor='black')
    fig_lucro_tempo.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray',
    showline=True, linewidth=1, linecolor='black')

    # Alterando a cor do fundo
    fig_lucro_tempo.layout.plot_bgcolor = '#F2F2F2'
    fig_lucro_tempo.layout.paper_bgcolor = '#F2F2F2'

    # Exportando o gráfico para html (como string)
    grafico_lucro_tempo=fig_lucro_tempo.to_html(full_html=False, config= {'displayModeBar': False, 'response':True})
    
    # Iniciando outro gráfico de lucro por seção
    lucro_secao=venda_produtos_cliente.groupby("secao").sum().sort_values('lucro', ascending=False ).reset_index()

    fig_lucro_secao = px.bar(lucro_secao, x="lucro", y="secao", color="secao", barmode = 'stack', color_discrete_map={'Açougue': '#EF553B', 
                                                   'Padaria': '#AB63FA', 'Produtos de Limpeza': '#FFA15A', 'Alimentos em Geral': '#00CC96'}, 
                labels={"lucro":"Lucro", "secao":"Seção"})
    fig_lucro_secao.update_layout(title = 'Lucros por seção', yaxis={'categoryorder':'total descending'}, 
    font = {'family': 'Arial','size': 14,'color': 'black'})



    # Alterando a cor do fundo
    fig_lucro_secao.layout.plot_bgcolor = '#F2F2F2'
    fig_lucro_secao.layout.paper_bgcolor = '#F2F2F2'

    # Exportando o gráfico para html (como string)
    grafico_barras_lucro_secao=fig_lucro_secao.to_html(full_html=False, config= {'displayModeBar': False, 'response':True})

    # Criando o dicionário de contexto com as informações para preencher o template (incluindo o gráfico)
    context = {
        "titulo": "Lucros por categoria",
        "legenda_pergunta":"Você já se perguntou qual é a nossa categoria de produtos mais lucrativa e como o lucro varia ao longo do mês?",
        "legenda_resposta":"Nessa página mostramos as estatísticas dos lucros de cada seção dos nossos produtos. É exibido qual categoria foi a mais lucrativa ao decorrer do mês de novembro de 2021, bem como esse lucro está distribuído ao longo dos dias. Como exposto, o açougue é o setor mais lucrativo, sendo seguido pela padaria. Contudo, essas disparidade acontece principalmente na primeira metade do mês, já que no fim, o lucro diminiu consideravelmente em todas as categorias. Ainda, nosso dia mais lucrativo foi 9 de novembro, uma terça-feira, que é o segundo dia da semana mais lucrativo no mês (mostrado em outras análises).",
        "botoes": [
            #['nome', 'link']
            ['Produtos mais vendidos','produtos_mais_vendidos'],
            ['Venda por dia da semana','venda_por_dia_da_semana'],
            ['Consumidores mais ativos','consumidores_mais_ativos'],
            ['Relação quantidade e receita bruta','relacao_quantidade_lucro_bruto']
        ],
        "graficos": [grafico_lucro_tempo, grafico_barras_lucro_secao]
        }

    # Retorna a página da visualização (com as informações desejadas)
    return render(request, "visualizacao1.html",context)
