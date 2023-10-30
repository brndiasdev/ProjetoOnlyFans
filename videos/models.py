from django.db import models
from django.contrib.auth.models import User
from perfil.models import Perfil, Meninas
# from PIL import Image
from django.utils import timezone
from datetime import datetime, date
from django.forms import ValidationError

class Videos(models.Model):
    menina = models.ForeignKey(Meninas, on_delete=models.CASCADE, verbose_name="Menina")
    link = models.CharField(default='', max_length=255, verbose_name="Link")
    nome = models.SlugField(unique=True, default='', max_length=255, verbose_name="Nome")
    descricao = models.TextField(default='', max_length=2000, verbose_name="Descricao")
    premium = models.BooleanField(default=False, verbose_name="Videos Premium")
    preco_premium = models.FloatField(default=0, verbose_name="Preço Premium")
    foto = models.ImageField(blank=True, null=True, upload_to='foto_videos/%Y/%m/%d', verbose_name="Foto")

    class Meta:
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'

    def __str__(self):
        return f'{self.nome}'
    

class Audios(models.Model):
    menina = models.ForeignKey(Meninas, on_delete=models.CASCADE, verbose_name="Menina")
    nome = models.CharField(unique=True, default='', max_length=255, verbose_name="Nome")
    arquivo = models.FileField(upload_to='audios/%Y/%m/%d', verbose_name="Audio")

    class Meta:
        verbose_name = 'Audio'
        verbose_name_plural = 'Audios'

    def __str__(self):
        return f'{self.nome}'
    

class Planos(models.Model):
    tres_meses = models.FloatField(default=0, verbose_name="Três meses")
    seis_meses = models.FloatField(default=0, verbose_name="Seis meses")
    um_mes = models.FloatField(default=0, verbose_name="Um mes")

    class Meta:
        verbose_name = 'Plano'
        verbose_name_plural = 'Planos'

    def __str__(self):
        return f'{self.tres_meses} -> {self.seis_meses} -> {self.um_mes}'
    

class Comentarios(models.Model):
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, verbose_name="Perfil")
    comentario = models.CharField(default='', max_length=500, verbose_name="Comentario")
    video = models.ForeignKey(Videos, on_delete=models.CASCADE, verbose_name="Video")
    visibilidade = models.BooleanField(default=False, verbose_name="Visibilidade")

    class Meta:
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'

    def __str__(self):
        return f'{self.perfil.nome}'


class Pedido(models.Model):
    comprador = models.ForeignKey(Perfil, on_delete=models.SET_NULL, 
                                          verbose_name="Comprador", blank=True, null=True)
    
    tipo_pagamento = models.CharField(default='', max_length=255, verbose_name="Tipo de pagamento", blank=True, null=True)
    preco_pedido = models.FloatField(default=0, verbose_name="Preço do pedido")
    data_pedido = models.DateTimeField(default=timezone.now, verbose_name="Data do pedido")

    data_vencimento = models.DateTimeField(verbose_name="Data do vencimento", blank=True, null=True)

    descricao_pagamento = models.CharField(default='', max_length=255, verbose_name="Descrição do pagamento", blank=True, null=True)
    plano = models.CharField(
		default='tres_meses',
		max_length=20,
		choices=(
			('tres_meses', 'tres_meses'),
			('seis_meses', 'seis_meses'),
            ('um_mes', 'um_mes'),
		), 
		verbose_name="Plano Escolhido"
	)
    status_pedido = models.CharField(
		default='pending',
		max_length=20,
		choices=(
			('approved', 'approved'),
			('rejected', 'rejected'),
            ('pending', 'pending'),
		), 
		verbose_name="Status Pedido"
	)
    IdTransaction = models.IntegerField(default=0, verbose_name="IdTransaction")
    parcelamentos = models.IntegerField(default=0, verbose_name="Parcelamentos")
    
    plano_ativo = models.BooleanField(default=False, verbose_name="Plano Ativo")

    recebeu_email_aprovado = models.BooleanField(default=False, verbose_name="Código Interno AP")
    recebeu_email_reprovado = models.BooleanField(default=False, verbose_name="Código Interno REP")
    recebeu_email_pendente = models.BooleanField(default=False, verbose_name="Código Interno PEN")

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    def __str__(self):
        return f'{self.comprador} -> {self.id}'
    

class PedidoVideoPremium(models.Model):
    comprador = models.ForeignKey(Perfil, on_delete=models.SET_NULL, 
                                          verbose_name="Comprador", blank=True, null=True)
    
    tipo_pagamento = models.CharField(default='', max_length=255, verbose_name="Tipo de pagamento", blank=True, null=True)
    preco_pedido = models.FloatField(default=0, verbose_name="Preço do pedido")
    data_pedido = models.DateTimeField(default=timezone.now, verbose_name="Data do pedido")
    descricao_pagamento = models.CharField(default='', max_length=255, verbose_name="Descrição do pagamento", blank=True, null=True)
        
    video = models.ForeignKey(Videos, on_delete=models.SET_NULL, 
                                          verbose_name="Video Premium", blank=True, null=True)

    status_pedido = models.CharField(
		default='pending',
		max_length=20,
		choices=(
			('approved', 'approved'),
			('rejected', 'rejected'),
            ('pending', 'pending'),
		), 
		verbose_name="Status Pedido"
	)
    IdTransaction = models.IntegerField(default=0, verbose_name="IdTransaction")
    parcelamentos = models.IntegerField(default=0, verbose_name="Parcelamentos")

    recebeu_email_aprovado = models.BooleanField(default=False, verbose_name="Código Interno AP")
    recebeu_email_reprovado = models.BooleanField(default=False, verbose_name="Código Interno REP")
    recebeu_email_pendente = models.BooleanField(default=False, verbose_name="Código Interno PEN")

    class Meta:
        verbose_name = 'Pedido Video Premium'
        verbose_name_plural = 'Pedidos Videos Premium'

    def __str__(self):
        return f'{self.comprador} -> {self.id}'