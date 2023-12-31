# Generated by Django 4.2.1 on 2023-06-05 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='videos',
            options={'verbose_name': 'Video', 'verbose_name_plural': 'Videos'},
        ),
        migrations.AddField(
            model_name='videos',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='fotos/%Y/%m/%d', verbose_name='Foto'),
        ),
    ]
