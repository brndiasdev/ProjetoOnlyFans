# Generated by Django 4.2.1 on 2023-07-03 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0023_audios'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audios',
            name='nome',
            field=models.CharField(default='', max_length=255, unique=True, verbose_name='Nome'),
        ),
    ]
