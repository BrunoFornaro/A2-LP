# Generated by Django 3.2.8 on 2021-12-02 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0005_alter_clientes_cpf'),
    ]

    operations = [
        migrations.AddField(
            model_name='produtos',
            name='imagem',
            field=models.CharField(default=1, max_length=60),
            preserve_default=False,
        ),
    ]
