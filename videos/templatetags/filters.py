from django import template
from videos.models import Videos, Comentarios, Audios, Pedido, PedidoVideoPremium, Perfil
from perfil.models import Perfil
from mutagen.mp3 import MP3
import os
from django.conf import settings
from pathlib import Path

register = template.Library()
caminho_local = Path(__file__).parent.parent

@register.filter(name='formatacao_slug')
def formatacao_slug(slug: str):
    slug_formatado = slug.replace('-', ' ')
    slug_formatado = slug_formatado.replace('cao', 'ção')
    return slug_formatado


@register.filter(name='video_numero_comentarios')
def video_numero_comentarios(video: Videos):
    comentarios = Comentarios.objects.filter(video__nome=video.nome, visibilidade=True)
    return len(comentarios)


@register.filter(name='video_numero_curtidas')
def video_numero_curtidas(video: Videos):
    comentarios = Comentarios.objects.filter(video__nome=video.nome, visibilidade=True)

    if len(comentarios) == 0:
        numero_curtidas = 5
    else:
        numero_curtidas = len(comentarios) + len(comentarios) * 3

    return numero_curtidas


@register.filter(name='tamanho_audio')
def tamanho_audio(audio: Audios):
    caminho = settings.MEDIA_ROOT / audio.arquivo.name
    _audio = MP3(caminho)
    duration_in_s = _audio.info.length
    minutos = int(duration_in_s / 60.0)
    minutos_formatado = int(duration_in_s / 60.0) if len(str(minutos)) != 1 else f'0{minutos}'
    segundos = int(duration_in_s % 60.0)
    return f'{minutos_formatado}:{segundos}'


@register.filter(name='pagou_premium')
def pagou_premium(video: Videos):
    ...


