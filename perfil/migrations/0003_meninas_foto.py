# Generated by Django 4.2.1 on 2023-06-18 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0002_meninas'),
    ]

    operations = [
        migrations.AddField(
            model_name='meninas',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='meninas/%Y/%m/%d', verbose_name='Foto'),
        ),
    ]