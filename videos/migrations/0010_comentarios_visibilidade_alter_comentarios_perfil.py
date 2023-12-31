# Generated by Django 4.2.1 on 2023-06-19 15:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0006_delete_comentarios'),
        ('videos', '0009_comentarios'),
    ]

    operations = [
        migrations.AddField(
            model_name='comentarios',
            name='visibilidade',
            field=models.BooleanField(default=False, verbose_name='Visibilidade'),
        ),
        migrations.AlterField(
            model_name='comentarios',
            name='perfil',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='perfil.perfil', verbose_name='Perfil'),
        ),
    ]
