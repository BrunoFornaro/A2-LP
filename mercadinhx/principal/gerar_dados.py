from numpy import random
import pandas as pd
import numpy as np
import random as rd
from faker import Faker
import json

fake = Faker("pt-BR")

def gerar_dados(quantidade_de_vendas = 500, quantidade_de_clientes = 200):

    # Tabela de produtos
    nome_dos_produtos = ["morango", "melancia", "banana", "uva", "batata", "berinjela", "abobrinha", "alface", "couve-flor", "feijão", "arroz", "macarrão", "alcatra", "maminha", "bisteca suína", "carré de cordeiro", "costela", "paleta suína", "picanha", "peito de frango", "bolo", "pão de forma", "pão de queijo", "pão francês", "pastel", "sanduíche", "sonho", "torta", "amaciante", "água sanitária", "detergente", "flanela", "odorizador", "rodo", "sabão em pó", "sabonete"]
    secao_dos_produtos = ["frutas_e_verduras", "frutas_e_verduras", "frutas_e_verduras", "frutas_e_verduras", "frutas_e_verduras", "frutas_e_verduras", "frutas_e_verduras", "frutas_e_verduras", "frutas_e_verduras", "frutas_e_verduras", "frutas_e_verduras", "frutas_e_verduras", "acougue", "acougue", "acougue", "acougue", "acougue", "acougue", "acougue", "acougue", "padaria", "padaria", "padaria", "padaria", "padaria", "padaria", "padaria", "padaria", "produtos_de_limpeza", "produtos_de_limpeza", "produtos_de_limpeza", "produtos_de_limpeza", "produtos_de_limpeza", "produtos_de_limpeza", "produtos_de_limpeza", "produtos_de_limpeza"]
    custo_dos_produtos = [4.30, 11.79, 2, 4.19, 2.39, 8.59, 2.69, 0.45, 3.19, 6.49, 3.19, 1.69, 23.19, 33.49, 15.73, 147.99, 16.39, 17.09, 43.35, 11.19, 17.89, 3.73, 17.04, 4.39, 3.19, 7.99, 1.79, 26.95, 5.19, 7.96, 1.3, 0.59, 14.38, 2.74, 6.15, 0.65]
    preco_produtos = [7.99, 15.99, 5.99, 7.47, 3.99, 11.99, 3.49, 0.98, 5.48, 8.45, 4.31, 2.48, 31.99, 42.99, 22.79, 172, 20.99, 23.99, 70.89, 16.49, 35, 6.99, 23.99, 10.99, 4.99, 12.99, 3.49, 45, 6.70, 11.98, 2.70, 1.99, 23.99, 5.99, 9.69, 1.29]
    prateleira_dos_produtos = ["1A", "1C", "1B", "1D", "2B", "2D", "2A", "2C", "2E", "3B", "3A", "3C", "4A", "4B", "5A", "5B", "5C", "5D", "4C", "4D", "6A", "7A", "7B", "7C", "7D", "7E", "6B", "6C", "8A", "8B", "8C", "9A", "9B", "9C", "8D", "9D"]
    estoque_produtos = [50, 20, 40, 36, 47, 12, 19, 25, 20, 43, 80, 38, 7, 9, 5, 5, 10, 9, 6, 10, 7, 15, 1, 3, 9, 15, 20, 7, 12, 8, 40, 32, 6, 10, 13, 58]
    unidade_de_medida_estoque = ["bandeja", "unidade", "kg", "bandeja", "kg", "kg", "kg", "pé", "pé", "kg", "kg", "pacote", "kg", "kg", "kg", "kg", "kg", "kg", "kg", "kg", "kg", "pacote", "kg", "kg", "unidade", "unidade", "unidade", "kg", "unidade", "unidade", "unidade", "unidade", "unidade", "unidade", "unidade", "unidade"]
    imagem = ["morango.jpg", "melancia.jpg", "banana.jpg", "uva.jpg", "batata.jpg", "beringela.jpg", "abobrinha.jpg", "alface.jpg", "couve_flor.jpg", "feijao.jpg", "arroz.jpg", "macarrao.jpg", "alcatra.jpg", "maminha.jpg", "bisteca_suina.jpg", "carre_de_cordeiro.jpg", "costela.jpg", "paleta_suina.jpg", "picanha.jpg", "peito_de_frango.jpg", "bolo.jpg", "pao_de_forma.jpg", "pao_de_queijo.jpg", "pao_frances.jpg", "pastel.jpg", "sanduiche.jpg", "sonho.jpg", "torta.jpg", "amaciante.jpg", "agua_sanitaria.jpg", "detergente.jpg", "flanela.jpg", "odorizador.jpg", "rodo.jpg", "sabao_em_po.jpg", "sabonete.jpg"]

    produtos = {
        "id": list(range(len(nome_dos_produtos))),
        "nome": nome_dos_produtos,
        "secao": secao_dos_produtos,
        "custo": custo_dos_produtos,
        "preco": preco_produtos,
        "prateleira": prateleira_dos_produtos,
        "estoque": estoque_produtos,
        "unidade_de_medida_de_estoque": unidade_de_medida_estoque,
        "imagem": imagem
    }

    produtos = pd.DataFrame(produtos)

    # Tabela de clientes
    clientes = {
        'id': list(range(quantidade_de_clientes)),
        'nome': [],
        'nascimento': [],
        'endereco':[],
        'cpf': [],
        'telefone': [],
        'usuario': [],
        'senha': []
    }

    for id in clientes['id']:
        clientes['nome'].append(fake.name())
        clientes['nascimento'].append(fake.date_of_birth(minimum_age = 18, maximum_age = 73))
        clientes['endereco'].append(fake.address())
        clientes['cpf'].append(fake.cpf())
        clientes['telefone'].append(fake.phone_number())
        clientes['usuario'].append(fake.user_name())
        clientes['senha'].append(fake.password(12))
    
    clientes = pd.DataFrame(clientes)

    # Tabela de vendas
    datas = np.arange(np.datetime64('2021-11-01'), np.datetime64('2021-12-01'))
    probabilidade = np.linspace(1, 2, num=datas.size)
    probabilidade = probabilidade / probabilidade.sum()
    datas = np.random.choice(datas, p=probabilidade, size=quantidade_de_vendas)
    datas.sort()
    vendas = {
        'id' : [],
        'id_clientes' : [],
        'data' : []
    }
    for id, data in enumerate(datas):
        vendas['id'].append(id)
        vendas['id_clientes'].append(np.random.choice(clientes['id']))
        vendas['data'].append(data)

    vendas = pd.DataFrame(vendas)
    vendas["data"] = vendas["data"].dt.strftime('%Y-%m-%d')

    # Tabela intermediária entre vendas e produtos
    venda_produtos = {
        'id_vendas' : [],
        'id_produtos' : [],
        'quantidade' : []
    }

    for id in range(quantidade_de_vendas):
        venda_produtos['id_vendas'].append(vendas['id'][id])
        venda_produtos['id_produtos'].append(np.random.choice(produtos['id']))
        venda_produtos['quantidade'].append(random.randint(1, 5))

    for id in range(4 * quantidade_de_vendas):
        venda_produtos['id_vendas'].append(np.random.choice(clientes['id']))
        venda_produtos['id_produtos'].append(np.random.choice(produtos['id']))
        venda_produtos['quantidade'].append(random.randint(1, 5))

    venda_produtos = pd.DataFrame(venda_produtos)
    
    return (produtos,clientes,vendas,venda_produtos)

dados = gerar_dados()
produtos = dados[0]
clientes = dados[1]
vendas = dados[2]
venda_produtos = dados[3]

produtos_json = []
for indice, linha in produtos.iterrows():
    produtos_json.append(
        {
            "id": str(linha["id"]),
            "model": "principal.Produtos",
            "fields": {
                "nome": str(linha["nome"]),
                "secao": str(linha["secao"]),
                "custo": str(linha["custo"]),
                "preco": str(linha["preco"]),
                "prateleira": str(linha["prateleira"]),
                "estoque": str(linha["estoque"]),
                "unidade_de_medida_de_estoque": str(linha["unidade_de_medida_de_estoque"]),
                "imagem": str(linha["imagem"])
            }
        }
    )

clientes_json = []
for indice, linha in clientes.iterrows():
    clientes_json.append(
        {
            "id": str(linha["id"]),
            "model": "principal.Clientes",
            "fields": {
                "nome": str(linha["nome"]),
                "nascimento": str(linha["nascimento"]),
                "endereco": str(linha["endereco"]),
                "cpf": str(linha["cpf"]),
                "telefone": str(linha["telefone"]),
                "usuario": str(linha["usuario"]),
                "senha": str(linha["senha"])
            }
        }
    )

vendas_json = []
for indice, linha in vendas.iterrows():
    vendas_json.append(
        {
            "id": str(linha["id"]),
            "model": "principal.Vendas",
            "fields": {
                "id_clientes": str(linha["id_clientes"]),
                "data": str(linha["data"])
            }
        }
    )

vendas_produtos_json = []
for indice, linha in venda_produtos.iterrows():
    vendas_produtos_json.append(
        {
            "id": str(indice),
            "model": "principal.VendasProdutos",
            "fields": {
                "id_vendas": str(linha["id_vendas"]),
                "id_produtos": str(linha["id_produtos"]),
                "quantidade": str(linha["quantidade"])
            }
        }
    )

with open('Produtos.json', 'w', encoding='utf-8') as f:
    json.dump(produtos_json, f,ensure_ascii=False)

with open('Clientes.json', 'w', encoding='utf-8') as f:
    json.dump(clientes_json, f,ensure_ascii=False)
    
with open('Vendas.json', 'w', encoding='utf-8') as f:
    json.dump(vendas_json, f,ensure_ascii=False)

with open('VendasProdutos.json', 'w', encoding='utf-8') as f:
    json.dump(vendas_produtos_json, f,ensure_ascii=False)


# preco = [31.99, 42.99, 22.79, 172, 20.99, 23.99, 70.89, 16.49, 45, 6.99, 23.99, 10.99, 4.99, 12.99, 3.49, 40, 6.70, 11.98, 2.70, 1.99, 23.99, 5.99, 9.69, 1.29]
# nome = ["alcatra", "maminha", "bisteca suína", "carré de cordeiro", 
# "costela", "paleta suína", "picanha", "peito de frango", "bolo", 
# "pão de forma", "pão de queijo", "pão fracês", "pastel", "sanduíche", 
# "sonho", "torta", "amaciante", "água sanitária", "detergente", "flanela", 
# "odorizador", "rodo", "sabão em pó", "sabonete"]
# prateleira = ["4A", "4B", "5A", "5B", "5C", "5D", "4C", "4D", "6A", "7A", "7B", "7C", "7D", "7E", "6B", "6C", "8A", "8B", "8C", "9A", "9B", "9C", "8D", "9D"]
# estoque = []
# unidade_de_medida = ["unidade",""]
# imagem = ["alcatra.jpg", "maminha.jpg", "bisteca_suina.jpg", "carre_de_cordeiro.jpg", "costela.jpg", "paleta_suina.jpg", "picanha.jpg", "peito_de_frango.jpg", "bolo.jpg", "pao_de_forma.jpg", "pao_de_queijo.jpg", "pao_fraces.jpg", "pastel.jpg", "sanduiche.jpg", "sonho.jpg", "torta.jpg", "amaciante.jpg", "agua_sanitaria.jpg", "detergente.jpg", "flanela.jpg", "odorizador.jpg", "rodo.jpg", "sabao_em_po.jpg", "sabonete.jpg"]
# secao = ["frutas_e_verduras", "frutas_e_verduras", "frutas_e_verduras", "frutas_e_verduras", "frutas_e_verduras", "frutas_e_verduras", "frutas_e_verduras", "frutas_e_verduras", "acougue", "acougue", "acougue", "acougue", "acougue", "acougue", "acougue", "acougue", "padaria", "padaria", "padaria", "padaria", "padaria", "padaria", "padaria", "padaria", "produtos_de_limpeza", "produtos_de_limpeza", "produtos_de_limpeza", "produtos_de_limpeza", "produtos_de_limpeza", "produtos_de_limpeza", "produtos_de_limpeza", "produtos_de_limpeza"]