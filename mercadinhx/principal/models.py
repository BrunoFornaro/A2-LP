from django.db import models
from django.shortcuts import SupportsGetAbsoluteUrl


# Create your models here.
class Produtos(models.Model):
    id = models.CharField()
    nome = models.CharField(max_length=80)
    preco = models.FloatField()
    prateleira = models.CharField()
    estoque = models.FloatField()
    unidade_de_medida_de_estoque = models.CharField()

class Clientes(models.Model):
    id = models.IntegerField()
    nome = models.CharField(max_length=80)
    nascimento = models.DateField()
    endereço = models.CharField(max_length=80)
    cpf = models.IntegerField()
    telefone = models.CharField()
    usuario = models.CharField()
    senha = models.CharField()

class Vendas(models.Model):
    id = models.IntegerField()
    id_cliente = models.IntegerField()
    data = models.DateField()

class VendasProdutos(models.Model):
    id_vendas = models.IntegerField()
    id_produto = models.IntegerField()
    quantidade = models.FloatField()