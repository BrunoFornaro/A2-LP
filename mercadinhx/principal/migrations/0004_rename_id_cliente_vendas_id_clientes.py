# Generated by Django 3.2.8 on 2021-12-02 14:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0003_rename_id_produto_vendasprodutos_id_produtos'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vendas',
            old_name='id_cliente',
            new_name='id_clientes',
        ),
    ]
