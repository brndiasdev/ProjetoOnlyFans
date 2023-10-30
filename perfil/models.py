from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuário")
    nome = models.CharField(default=None, max_length=255, verbose_name="Nome")
    email = models.CharField(default=None, max_length=255, verbose_name="Email")

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'

    def __str__(self):
        return f'{self.nome}'
    

class Meninas(models.Model):
    nome = models.CharField(unique=True, default=None, max_length=255, verbose_name="Nome")
    email = models.CharField(default=None, max_length=255, verbose_name="Email")
    foto = models.ImageField(blank=True, null=True, upload_to='meninas/%Y/%m/%d', verbose_name="Foto")

    class Meta:
        verbose_name = 'Menina'
        verbose_name_plural = 'Meninas'

    def __str__(self):
        return f'{self.nome}'