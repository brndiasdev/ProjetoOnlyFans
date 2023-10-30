from django.shortcuts import render, redirect
from videos.models import Planos, Pedido
from perfil.models import Perfil

def home(request):
    if not Planos.objects.filter().exists():
        tres_meses = 0
        seis_meses = 0
        um_mes = 0
        planos = None
    else:
        planos = Planos.objects.filter().first()
        tres_meses = planos.tres_meses
        seis_meses = planos.seis_meses
        um_mes = planos.um_mes

    if request.user.is_authenticated:
        if Perfil.objects.filter(usuario=request.user).exists():
            perfil = Perfil.objects.get(usuario=request.user)
            if Pedido.objects.filter(comprador=perfil, status_pedido='approved', plano_ativo=True).exists():
                return redirect('videos')

    if planos:
        if len(str(round(planos.tres_meses, 2))) <= 4:
            tres_meses = str(round(planos.tres_meses, 2)) + '0'
            tres_meses = str(tres_meses.replace('.', ','))
        else:
            tres_meses = str(round(planos.tres_meses, 2)).replace('.', ',')

        if len(str(round(planos.seis_meses, 2))) <= 4:
            seis_meses = str(round(planos.seis_meses, 2)) + '0'
            seis_meses = str(seis_meses.replace('.', ','))
        else:
            seis_meses = str(round(planos.seis_meses, 2)).replace('.', ',')

        if len(str(round(planos.um_mes, 2))) <= 4:
            um_mes = str(round(planos.um_mes, 2)) + '0'
            um_mes = str(um_mes.replace('.', ','))
        else:
            um_mes = str(round(planos.um_mes, 2)).replace('.', ',')

    return render(request, 'index.html', {
        'tres_meses': tres_meses,
        'seis_meses': seis_meses,
        'um_mes': um_mes,
    })


def escolher_plano(request, plano):
    if not request.session.get('plano'):
        request.session['plano'] = {}

    if plano == 'tres_meses':
        request.session['plano'] = 'tres_meses'
    elif plano == 'seis_meses':
        request.session['plano'] = 'seis_meses'
    else:
        request.session['plano'] = 'um_mes'

    request.session.save()
    if request.user.is_authenticated:
        return redirect('area_pagamento')
    else:
        return redirect('registro')
