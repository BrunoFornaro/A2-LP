from django.db import models

# Create your models here.
class Produtos(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=80)
    secao = models.CharField(max_length=60)
    custo = models.FloatField()
    preco = models.FloatField()
    prateleira = models.CharField(max_length=10)
    estoque = models.FloatField()
    unidade_de_medida_de_estoque = models.CharField(max_length=80)
    imagem = models.CharField(max_length=60)


class Clientes(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=80)
    nascimento = models.DateField()
    endereco = models.CharField(max_length=80)
    cpf = models.CharField(max_length=14)
    telefone = models.CharField(max_length=20)
    usuario = models.CharField(max_length=30)
    senha = models.CharField(max_length=30)


class Vendas(models.Model):
    id = models.IntegerField(primary_key=True)
    id_clientes = models.IntegerField()
    data = models.DateField()


class VendasProdutos(models.Model):
    id = models.IntegerField(primary_key=True)
    id_vendas = models.IntegerField()
    id_produtos = models.IntegerField()
    quantidade = models.FloatField()
