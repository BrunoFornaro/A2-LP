# Generated by Django 3.2.8 on 2021-12-02 14:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clientes',
            old_name='endereço',
            new_name='endereco',
        ),
    ]
