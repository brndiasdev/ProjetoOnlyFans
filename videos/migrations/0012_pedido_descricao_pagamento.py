# Generated by Django 4.2.1 on 2023-06-24 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0011_pedido_idtransaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='descricao_pagamento',
            field=models.CharField(default='', max_length=255, verbose_name='Descrição do pagamento'),
        ),
    ]
