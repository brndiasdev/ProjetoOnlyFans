# Generated by Django 4.2.1 on 2023-06-26 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0018_alter_planos_doze_meses_alter_planos_seis_meses_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='data_vencimento',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Data do vencimento'),
        ),
    ]
