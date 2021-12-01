from numpy import random
import pandas as pd
import numpy as np
import random as rd
from faker import Faker

fake = Faker("pt-BR")

def gerar_dados(quantidade_de_vendas = 500, quantidade_de_clientes = 200):

    # Tabela de produtos
    nome_dos_produtos = ["morango", "melancia", "banana", "uva", "batata", "berinjela", "abobrinha", "alface", "couve-flor", "feijão", "arroz", "macarrão"]
    preco_produtos = [7.99, 1.49, 5.99, 7.47, 3.99, 11.99, 3.50, 0.98, 5.48, 8.45, 20.31, 2.48]
    prateleira_dos_produtos = ["1A", "1C", "1B", "1D", "2B", "2D", "2A", "2C", "2E", "3B", "3A", "3C"]
    estoque_produtos = [50, 20, 40, 36, 47, 12, 19, 25, 20, 43, 80, 38]
    unidade_de_medida_estoque = ["bandejas", "unidades", "kg", "bandejas", "kg", "kg", "kg", "pés", "pés", "kg", "kg", "pacotes"]
    imagem = ["morango-alt.png", "melancia.jpg", "banana.png", "uva-alt.png", "batata.JPEG", "beringela.jpg", "abobrinha.JPEG", "alface.png", "couve-flor.png", "feijao.png", "arroz.png", "macarrao.png"]

    produtos = {
        "id": list(range(len(nome_dos_produtos))),
        "nome": nome_dos_produtos,
        "preco": preco_produtos,
        "prateleira": prateleira_dos_produtos,
        "estoque": estoque_produtos,
        "unidade_de_medida_de_estoque": unidade_de_medida_estoque
    }

    produtos = pd.DataFrame(produtos)

    # Tabela de clientes
    clientes = {
        'id': list(range(quantidade_de_clientes)),
        'nome': [],
        'idade': [],
        'endereço':[],
        'cpf': [],
        'telefone': [],
        'usuario': [],
        'senha': []
    }

    for id in clientes['id']:
        clientes['nome'].append(fake.name())
        clientes['idade'].append(random.randint(18, 73))
        clientes['endereço'].append(fake.address())
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
        'id_cliente' : [],
        'data' : []
    }
    for id, data in enumerate(datas):
        vendas['id'].append(id)
        vendas['id_cliente'].append(np.random.choice(clientes['id']))
        vendas['data'].append(data)

    vendas = pd.DataFrame(vendas)

    # Tabela intermediária entre vendas e produtos
    venda_produtos = {
        'id_vendas' : [],
        'id_produto' : [],
        'quantidade' : []
    }

    for id in range(quantidade_de_vendas):
        venda_produtos['id_vendas'].append(vendas['id'][id])
        venda_produtos['id_produto'].append(np.random.choice(produtos['id']))
        venda_produtos['quantidade'].append(random.randint(1, 5))

    for id in range(4 * quantidade_de_vendas):
        venda_produtos['id_vendas'].append(np.random.choice(clientes['id']))
        venda_produtos['id_produto'].append(np.random.choice(produtos['id']))
        venda_produtos['quantidade'].append(random.randint(1, 5))

    venda_produtos = pd.DataFrame(venda_produtos)

    return (produtos,clientes,vendas,venda_produtos)