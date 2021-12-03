from django.db import models
from django.forms.models import model_to_dict
import pandas as pd

def converter_query(instancia, retornar="lista_de_dicionarios"):
    context = []
    for entrada in instancia:
        entrada = model_to_dict(entrada)
        entrada["id"] = entrada["id"] - 1
        context.append(entrada)
    if retornar == "dataframe":
        context = pd.DataFrame(context)
    return context


# Create your models here.
class Produtos(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=80)
    preco = models.FloatField()
    prateleira = models.CharField(max_length=10)
    estoque = models.FloatField()
    unidade_de_medida_de_estoque = models.CharField(max_length=80)
    imagem = models.CharField(max_length=60)
    
    def pegar_dados(self, retornar="lista_de_dicionarios"):
        instancia = Produtos.objects.all()
        context = converter_query(instancia, retornar)
        return context

class Clientes(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=80)
    nascimento = models.DateField()
    endereco = models.CharField(max_length=80)
    cpf = models.CharField(max_length=14)
    telefone = models.CharField(max_length=20)
    usuario = models.CharField(max_length=30)
    senha = models.CharField(max_length=30)

    def pegar_dados(retornar="lista_de_dicionarios"):
        instancia = Clientes.objects.all()
        context = converter_query(instancia, retornar)
        return context


class Vendas(models.Model):
    id = models.IntegerField(primary_key=True)
    id_clientes = models.IntegerField()
    data = models.DateField()

    def pegar_dados(retornar="lista_de_dicionarios"):
        instancia = Vendas.objects.all()
        context = converter_query(instancia, retornar)
        return context


class VendasProdutos(models.Model):
    id = models.IntegerField(primary_key=True)
    id_vendas = models.IntegerField()
    id_produtos = models.IntegerField()
    quantidade = models.FloatField()

    def pegar_dados(retornar="lista_de_dicionarios"):
        instancia = VendasProdutos.objects.all()
        context = converter_query(instancia, retornar)
        return context