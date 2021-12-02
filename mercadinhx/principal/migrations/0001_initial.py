# Generated by Django 3.2.8 on 2021-12-02 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clientes',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=80)),
                ('nascimento', models.DateField()),
                ('endereço', models.CharField(max_length=80)),
                ('cpf', models.IntegerField()),
                ('telefone', models.CharField(max_length=20)),
                ('usuario', models.CharField(max_length=30)),
                ('senha', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Produtos',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=80)),
                ('preco', models.FloatField()),
                ('prateleira', models.CharField(max_length=10)),
                ('estoque', models.FloatField()),
                ('unidade_de_medida_de_estoque', models.CharField(max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='Vendas',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('id_cliente', models.IntegerField()),
                ('data', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='VendasProdutos',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('id_vendas', models.IntegerField()),
                ('id_produto', models.IntegerField()),
                ('quantidade', models.FloatField()),
            ],
        ),
    ]
