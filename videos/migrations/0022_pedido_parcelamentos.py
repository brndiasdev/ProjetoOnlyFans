# Generated by Django 4.2.1 on 2023-06-29 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0021_alter_pedido_data_vencimento'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='parcelamentos',
            field=models.IntegerField(default=0, verbose_name='Parcelamentos'),
        ),
    ]
