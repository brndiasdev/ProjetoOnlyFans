from django.shortcuts import render, redirect, reverse
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from .models import Perfil, Meninas
from videos.models import Videos, Comentarios, Pedido, Planos, Audios, PedidoVideoPremium
from django.http import Http404, HttpResponse
import copy
from django.db import connection
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string	
from django.utils.html import strip_tags	
from django.conf import settings
from pprint import pprint
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from pytz import timezone
import random
import requests
import json
import string
import qrcode
from django.views.decorators.csrf import csrf_exempt
from onlyfans.settings import DOMINIO, TOKEN, SECRET_KEY, SANDBOX, STATIC_ROOT
from faker import Faker

def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method != 'POST':
        return render(request, 'login.html')

    email = request.POST.get('email')
    senha = request.POST.get('senha')

    if not Perfil.objects.filter(email=email).exists() or not User.objects.filter(email=email).exists():
        messages.error(request, 'O E-mail informado não está atrelado a nenhuma conta!')
        return render(request, 'login.html')

    username = User.objects.get(email=email).username
    user = auth.authenticate(request, username=username, password=senha)

    if not user:
        messages.error(request, 'Usuário ou senha inválidos')
        return render(request, 'login.html')
    

    auth.login(request, user)
    return redirect('videos')


def logout(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    auth.logout(request)
    messages.success(request, 'Você fez o logout com sucesso!')
    return redirect('login')


def registro(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method != 'POST':
        return render(request, 'registro.html')

    usuario = request.POST.get('usuario')
    email = request.POST.get('email')
    nome = request.POST.get('nome')
    senha1 = request.POST.get('senha1')

    if not email or not nome or not usuario:
        messages.error(request, 'Nenhum campo pode ficar vazio!')
        return render(request, 'registro.html')
    
    if len(nome) >= 60:
        messages.error(request, 'Digite um nome com 30 caracteres ou menos!')
        return render(request, 'registro.html')
    
    if len(usuario) > 8:
        messages.error(request, 'Digite um usuário com 8 caracteres ou menos!')
        return render(request, 'registro.html')
    
    """ if senha1 != senha2:
        messages.error(request, 'As senhas precisam ser iguais!')
        return render(request, 'registro.html') """
    
    if len(senha1) < 4:
        messages.error(request, 'A senha precisa ter mo mínimo 4 caracteres!')
        return render(request, 'registro.html')

    try:
        validate_email(email)
    except:
        messages.error(request, 'E-mail inválido!')
        return render(request, 'registro.html')
    
    """ link = f'https://api.usebouncer.com/v1/email/verify?email={email}&timeout=10'
    headers = {
        "Accept": "application/json",
        'x-api-key': KEY_API_USEBOUNCER,
    }
    requisicao = requests.get(link, headers=headers)

    if str(requisicao) != '<Response [200]>':
        messages.error(request, 'No momento não foi possível criar a sua conta. Tente novamente mais tarde!')
        return render(request, 'registro.html')
    
    status = dict(requisicao.json())['reason']
    if status != 'accepted_email':
        messages.error(request, 'O E-mail informado NÃO existe!')
        return render(request, 'registro.html') """

    if User.objects.filter(email=email).exists() or Perfil.objects.filter(email=email).exists():
        messages.error(request, 'O E-mail informado já está sendo utilizado!')
        return render(request, 'registro.html')
    
    if User.objects.filter(username=usuario).exists():
        messages.error(request, 'O usuário informado já está sendo utilizado!')
        return render(request, 'registro.html')

    messages.success(request, 'Registrado com sucesso!')

    usuario = User.objects.create_user(email=email, username=usuario, password=senha1)
    usuario.save()
    perfil = Perfil.objects.create(usuario=usuario, email=email, nome=nome) 
    perfil.save()

    auth.login(request, usuario)
    return redirect('videos')



""" def verificacao_planos(pedido: Pedido):
    data_pedido = pedido.data_pedido

    ano_pedido = int(data_pedido.strftime('%Y'))
    mes_pedido = int(data_pedido.strftime('%m'))
    dia_pedido = int(data_pedido.strftime('%d'))

    data_atual = datetime.now()

    ano_atual = int(data_atual.strftime('%Y'))
    mes_atual = int(data_atual.strftime('%m'))
    dia_atual = int(data_atual.strftime('%d'))

    # delta = timedelta(hours=3)
    # data_pedido-=delta

    print(f'Data pedido: {data_pedido}')
    print(f'Ano pedido: {ano_pedido}')
    print(f'Mes pedido: {mes_pedido}')
    print(f'Dia pedido: {dia_pedido}')
    print()
    print(f'Data atual: {data_atual}')
    print(f'Ano atual: {ano_atual}')
    print(f'Mes atual: {mes_atual}')
    print(f'Dia atual: {dia_atual}')
    print()
    print(f'Data pedido: {type(data_pedido)}')
    print(f'Data atual: {type(data_atual)}')

    # 10/02/2023

    # 15/04/2023

    # 10/05/2023

    if pedido.plano == 'tres_meses':
        if ano_pedido == ano_atual and mes_atual - mes_pedido < 3 and mes_atual - mes_pedido >= 0:
            return True
        elif ano_pedido - ano_atual == 1 and (12 - mes_pedido + mes_atual) < 3:
            return True
        else:
            pedido.plano_ativo = False
            pedido.save()
            return False

    elif pedido.plano == 'seis_meses':
        if ano_pedido == ano_atual and mes_atual - mes_pedido < 6 and mes_atual - mes_pedido >= 0:
            return True
        elif ano_pedido - ano_atual == 1 and (12 - mes_pedido + mes_atual) < 6:
            return True
        else:
            pedido.plano_ativo = False
            pedido.save()
            return False

    else:
        if ano_atual - ano_pedido <= 0:
            return True
        elif ano_atual - ano_pedido >= 1 and (12 - mes_pedido + mes_atual) < 12:
            return True
        else:
            pedido.plano_ativo = False
            pedido.save()
            return False """
        

def verificacao_planos(pedido: Pedido):
    data_pedido = pedido.data_pedido
    data_vencimento = pedido.data_vencimento

    data_atual = datetime.now(timezone('America/Sao_Paulo'))

    if not data_vencimento:
        return False
    
    if data_atual > data_vencimento:
        pedido.plano_ativo = False
        pedido.save()
        return False
    else:
        return True


def area_pagamento(request):
    if not request.user.is_authenticated:
        return redirect('home')
    
    planos = None
    if not Planos.objects.filter().exists():
        preco_plano = 0
        plano = ''
    elif request.session.get('plano'):
        preco_plano = request.session['plano']
        planos = Planos.objects.filter().first()
    
        if request.session.get('plano') == 'tres_meses':
            preco_plano = planos.tres_meses
            plano = 'tres_meses'
        elif request.session.get('plano') == 'seis_meses':
            preco_plano = planos.seis_meses
            plano = 'seis_meses'
        else:
            preco_plano = planos.um_mes
            plano = 'um_mes'
    else:
        planos = Planos.objects.filter().first()
        preco_plano = 0
        plano = ''

    if preco_plano:
        if len(str(round(preco_plano, 2))) <= 4:
            preco_plano = str(round(preco_plano, 2)) + '0'
        else:
            preco_plano = round(preco_plano, 2)
    
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
    
    if not Perfil.objects.filter(usuario=request.user).exists():
        perfil = Perfil.objects.create(usuario=request.user, email=request.user.email, nome=request.user.usuario) 
        perfil.save()
    
    perfil = Perfil.objects.get(usuario=request.user)

    if Pedido.objects.filter(comprador=perfil, plano_ativo=True, status_pedido='approved').exists():
        pedido = Pedido.objects.filter(comprador=perfil, plano_ativo=True, status_pedido='approved').first()
        validador = verificacao_planos(pedido)
        if validador:
            return redirect('videos')
        else:
            messages.error(request, 'Infelizmente, o período do seu plano chegou ao fim. Para continuar desfrutando de todo o conteúdo exclusivo por mais tempo, recomendamos que você renove seu plano.')
    elif request.method != 'POST':
        messages.info(request, f'{request.user.username}, você não tem nenhum plano ativo. Para desfrutar de todo o conteúdo exclusivo, realize o pagamento do plano escolhido.')

    if request.method != 'POST':
        return render(request, 'area_pagamento.html', {
            'preco_plano': preco_plano,
            'plano': plano,
            'preco_tres_meses': tres_meses,
            'preco_seis_meses': seis_meses,
            'preco_um_mes': um_mes,
        })
    
    tipo_pagamento = request.POST.get('tipo-pagamento')
    if not plano:
        plano = request.POST.get('plano')
        if not plano or not tipo_pagamento:
            messages.info(request, f'{request.user.username}, você não tem nenhum plano ativo. Para desfrutar de todo o conteúdo exclusivo, realize o pagamento do plano escolhido.')
            messages.error(request, 'Preencha todos os campos!')
            return render(request, 'area_pagamento.html', {
                'preco_plano': preco_plano,
                'plano': plano,
                'preco_tres_meses': tres_meses,
                'preco_seis_meses': seis_meses,
                'preco_um_mes': um_mes,
            })
    else:
        if not tipo_pagamento:
            messages.info(request, f'{request.user.username}, você não tem nenhum plano ativo. Para desfrutar de todo o conteúdo exclusivo, realize o pagamento do plano escolhido.')
            messages.error(request, 'Preencha todos os campos!')
            return render(request, 'area_pagamento.html', {
                'preco_plano': preco_plano,
                'plano': plano,
                'preco_tres_meses': tres_meses,
                'preco_seis_meses': seis_meses,
                'preco_um_mes': um_mes,
            })
        
    if plano == 'tres_meses':
        preco_pedido = planos.tres_meses
    elif plano == 'seis_meses':
        preco_pedido = planos.seis_meses
    else:
        preco_pedido = planos.um_mes

    if tipo_pagamento == 'pix':
        url = "https://payment.safe2pay.com.br/v2/Payment"

        _plano = plano.replace('_', ' ').capitalize().replace('Tres', 'Três')

        payload = {
            "IsSandbox": SANDBOX,
            "Application": f"Cachorrinhas - {_plano}",
            "Vendor": "Lucas",
            "CallbackUrl": "https://cachorrinha.com.br/perfil/payment_status/",
            "PaymentMethod": "6",
            "Reference": f"{perfil.id} -> {perfil.usuario.username} -> {_plano}",
            "Customer": {
                "Name": f"{perfil.usuario.username} -> {perfil.nome}",
                "Identity": "31037942000178", # CPF/CNPJ
                "Email": f"{perfil.email}",
                "Address": {
                    "ZipCode": "90670090",
                    "Street": "Logradouro",
                    "Number": "123",
                    "Complement": "Complemento",
                    "District": "Higienopolis",
                    "CityName": "Porto Alegre",
                    "StateInitials": "RS",
                    "CountryName": "Brasil"
                }
            },
            "Products": [
                {
                    "Code": f"{perfil.id}",
                    "Description": f"{_plano}",
                    "UnitPrice": preco_pedido,
                    "Quantity": 1,
                },
            ],
        }

        headers = {
            'content-type': "application/json",
            'x-api-key': TOKEN,
        }

        response = requests.post(url, data=json.dumps(payload), headers=headers).json()

        if response.get('HasError'):
            messages.info(request, f'{request.user.username}, você não tem nenhum plano ativo. Para desfrutar de todo o conteúdo exclusivo, realize o pagamento do plano escolhido.')
            messages.error(request, response.get('Error'))
            return render(request, 'area_pagamento.html', {
                'preco_plano': preco_plano,
                'plano': plano,
                'preco_tres_meses': tres_meses,
                'preco_seis_meses': seis_meses,
                'preco_um_mes': um_mes,
            })
        elif response.get('ResponseDetail'):
            try:
                id_transaction = response.get('ResponseDetail').get('IdTransaction')
                message = response.get('ResponseDetail').get('Message')
                description = response.get('ResponseDetail').get('Description')
                status = response.get('ResponseDetail').get('Status')
                link = response.get('ResponseDetail').get('QrCode')
                codigo_pix = response.get('ResponseDetail').get('Key')
            except:
                messages.info(request, f'{request.user.username}, você não tem nenhum plano ativo. Para desfrutar de todo o conteúdo exclusivo, realize o pagamento do plano escolhido.')
                messages.error(request, 'Ocorreu algum erro com o seu pagamento. Tente novamente!')
                return render(request, 'area_pagamento.html', {
                    'preco_plano': preco_plano,
                    'plano': plano,
                    'preco_tres_meses': tres_meses,
                    'preco_seis_meses': seis_meses,
                    'preco_um_mes': um_mes,
                })
        else:
            messages.info(request, f'{request.user.username}, você não tem nenhum plano ativo. Para desfrutar de todo o conteúdo exclusivo, realize o pagamento do plano escolhido.')
            messages.error(request, 'Ocorreu algum erro com o seu pagamento. Tente novamente!')
            return render(request, 'area_pagamento.html', {
                'preco_plano': preco_plano,
                'plano': plano,
                'preco_tres_meses': tres_meses,
                'preco_seis_meses': seis_meses,
                'preco_um_mes': um_mes,
            })
        
        if status == '1' or status == 1:

            pedido = Pedido.objects.create(
                comprador=perfil,
                tipo_pagamento='pix',
                preco_pedido=preco_pedido,
                descricao_pagamento=description,
                plano=plano,
                IdTransaction=id_transaction,
            )
            
            html_content = render_to_string('email_pagamento_pendente_pix.html', {
                'usuario': request.user.username,
                'plano': _plano,
                'codigo_pix': codigo_pix,
                'link': link,
                'description': 'Iniciado uma transação pelo comprador. Por favor, realize o pagamento.'
            })
            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives('Pagamento pendente - Cachorrinhas', text_content, 
            settings.EMAIL_HOST_USER, [perfil.email])
            email.attach_alternative(html_content, 'text/html')
            email.send()

            pedido.recebeu_email_pendente = True
            pedido.save()

            """ qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=1,
            )
            qr.add_data(link)
            qr.make(fit=True)
            imagem = qr.make_image(fill_color='black', back_color='white')
            imagem.save(f'{STATIC_ROOT}/pix/qrcode.png') """

            request.session['codigo_pix'] = codigo_pix
            # request.session['link'] = f'/static/pix/qrcode.png'
            request.session['link'] = link
            request.session.save()
            
            return redirect('pendente_pix')

        elif status == '3' or status == 3:
            pedido = Pedido.objects.create(
                comprador=perfil,
                tipo_pagamento='pix',
                preco_pedido=preco_pedido,
                descricao_pagamento=description,
                plano=plano,
                IdTransaction=id_transaction,
                status_pedido='approved',
            )

            if plano == 'tres_meses':
                data_validade = pedido.data_pedido + relativedelta(months=3)
            elif plano == 'seis_meses':
                data_validade = pedido.data_pedido + relativedelta(months=6)
            else:
                data_validade = pedido.data_pedido + relativedelta(months=1)
            
            pedido.data_vencimento = data_validade

            html_content = render_to_string('email_pagamento_sucesso.html', {
                'usuario': request.user.username,
                'plano': _plano,
                'data_pedido': pedido.data_pedido.strftime('%d/%m/%Y'),
                'data_validade': pedido.data_vencimento.strftime('%d/%m/%Y'),
                'link': f'{DOMINIO}/perfil/',
            })
            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives('Pagamento aprovado - Cachorrinhas', text_content, 
            settings.EMAIL_HOST_USER, [perfil.email])
            email.attach_alternative(html_content, 'text/html')
            email.send()

            pedido.recebeu_email_aprovado = True
            pedido.plano_ativo = True
            pedido.save()

            return redirect('sucesso')

        else:
            messages.info(request, f'{request.user.username}, você não tem nenhum plano ativo. Para desfrutar de todo o conteúdo exclusivo, realize o pagamento do plano escolhido.')
            messages.error(request, 'Ocorreu algum erro com o seu pagamento. Tente novamente!')
            return render(request, 'area_pagamento.html', {
                'preco_plano': preco_plano,
                'plano': plano,
                'preco_tres_meses': tres_meses,
                'preco_seis_meses': seis_meses,
                'preco_um_mes': um_mes,
            })

    elif tipo_pagamento == 'cartao':
        nome_cartao = request.POST.get('nome_cartao')
        numero_cartao = request.POST.get('numero_cartao')
        data_expiracao = request.POST.get('data_expiracao')
        numero_parcelas = request.POST.get('numero_parcelas')
        codigo_cartao = request.POST.get('codigo_cartao')

        if not nome_cartao or not numero_cartao or not data_expiracao or not numero_parcelas or not codigo_cartao:
            messages.info(request, f'{request.user.username}, você não tem nenhum plano ativo. Para desfrutar de todo o conteúdo exclusivo, realize o pagamento do plano escolhido.')
            messages.error(request, 'Preencha todos os campos do cartão!')
            return render(request, 'area_pagamento.html', {
                'preco_plano': preco_plano,
                'plano': plano,
                'preco_tres_meses': tres_meses,
                'preco_seis_meses': seis_meses,
                'preco_um_mes': um_mes,
            })
        
        lista = [x for x in data_expiracao]
        lista.insert(3, '20')
        data_expiracao = ''.join(lista)
        
        url = "https://payment.safe2pay.com.br/v2/Payment"

        _plano = plano.replace('_', ' ').capitalize().replace('Tres', 'Três')

        payload = {
            "IsSandbox": SANDBOX,
            "Application": f"Cachorrinhas - {_plano}",
            "Vendor": "Lucas",
            "CallbackUrl": "https://cachorrinha.com.br/perfil/payment_status/",
            "PaymentMethod": "2",
            "Reference": f"{perfil.id} -> {perfil.usuario.username} -> {_plano}",
            "Customer": {
                "Name": f"{perfil.usuario.username} -> {perfil.nome}",
                "Identity": "31037942000178", # CPF/CNPJ
                "Email": f"{perfil.email}",
                "Address": {
                    "ZipCode": "90670090",
                    "Street": "Logradouro",
                    "Number": "123",
                    "Complement": "Complemento",
                    "District": "Higienopolis",
                    "CityName": "Porto Alegre",
                    "StateInitials": "RS",
                    "CountryName": "Brasil"
                }
            },
            "Products": [
                {
                    "Code": f"{perfil.id}",
                    "Description": f"{_plano}",
                    "UnitPrice": preco_pedido,
                    "Quantity": 1,
                },
            ],
            "PaymentObject": {
                "Holder": nome_cartao,
                "CardNumber": numero_cartao,
                "ExpirationDate": f'{data_expiracao}',
                "SecurityCode": f'{codigo_cartao}',
                "InstallmentQuantity": numero_parcelas,
            }
        }

        headers = {
            'content-type': "application/json",
            'x-api-key': TOKEN,
        }

        response = requests.post(url, data=json.dumps(payload), headers=headers).json()


        if response.get('HasError'):
            messages.info(request, f'{request.user.username}, você não tem nenhum plano ativo. Para desfrutar de todo o conteúdo exclusivo, realize o pagamento do plano escolhido.')
            messages.error(request, response.get('Error'))
            return render(request, 'area_pagamento.html', {
                'preco_plano': preco_plano,
                'plano': plano,
                'preco_tres_meses': tres_meses,
                'preco_seis_meses': seis_meses,
                'preco_um_mes': um_mes,
            })
        elif response.get('ResponseDetail'):
            try:
                id_transaction = response.get('ResponseDetail').get('IdTransaction')
                message = response.get('ResponseDetail').get('Message')
                description = response.get('ResponseDetail').get('Description')
                status = response.get('ResponseDetail').get('Status')
            except:
                messages.info(request, f'{request.user.username}, você não tem nenhum plano ativo. Para desfrutar de todo o conteúdo exclusivo, realize o pagamento do plano escolhido.')
                messages.error(request, 'Ocorreu algum erro com o seu pagamento. Tente novamente!')
                return render(request, 'area_pagamento.html', {
                    'preco_plano': preco_plano,
                    'plano': plano,
                    'preco_tres_meses': tres_meses,
                    'preco_seis_meses': seis_meses,
                    'preco_um_mes': um_mes,
                })

        if status == '3' or status == 3:
            pedido = Pedido.objects.create(
                comprador=perfil,
                tipo_pagamento='cartao',
                preco_pedido=preco_pedido,
                descricao_pagamento=description,
                plano=plano,
                parcelamentos=numero_parcelas,
                IdTransaction=id_transaction,
                status_pedido='approved',
            )

            if plano == 'tres_meses':
                data_validade = pedido.data_pedido + relativedelta(months=3)
            elif plano == 'seis_meses':
                data_validade = pedido.data_pedido + relativedelta(months=6)
            else:
                data_validade = pedido.data_pedido + relativedelta(months=1)
            
            pedido.data_vencimento = data_validade

            html_content = render_to_string('email_pagamento_sucesso.html', {
                'usuario': request.user.username,
                'plano': _plano,
                'data_pedido': pedido.data_pedido.strftime('%d/%m/%Y'),
                'data_validade': pedido.data_vencimento.strftime('%d/%m/%Y'),
                'link': f'{DOMINIO}/perfil/',
            })
            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives('Pagamento aprovado - Cachorrinhas', text_content, 
            settings.EMAIL_HOST_USER, [perfil.email])
            email.attach_alternative(html_content, 'text/html')
            email.send()

            pedido.recebeu_email_aprovado = True
            pedido.plano_ativo = True
            pedido.save()

            return redirect('sucesso')

        if status == '5' or status == 5:

            pedido = Pedido.objects.create(
                comprador=perfil,
                tipo_pagamento='cartao',
                preco_pedido=preco_pedido,
                descricao_pagamento=description,
                plano=plano,
                parcelamentos=numero_parcelas,
                IdTransaction=id_transaction,
            )
            
            html_content = render_to_string('email_pagamento_pendente.html', {
                'usuario': request.user.username,
                'plano': _plano,
                'description': 'Dentro do prazo de liberação da transação, você abriu uma disputa para fins de contestação da transação.',
            })
            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives('Pagamento pendente - Cachorrinhas', text_content, 
            settings.EMAIL_HOST_USER, [perfil.email])
            email.attach_alternative(html_content, 'text/html')
            email.send()

            pedido.recebeu_email_pendente = True
            pedido.save()

            messages.info(request, 'Dentro do prazo de liberação da transação, você abriu uma disputa para fins de contestação da transação.')
            return redirect('pendente')
        
        if status == '6' or status == 6:

            pedido = Pedido.objects.create(
                comprador=perfil,
                tipo_pagamento='cartao',
                preco_pedido=preco_pedido,
                descricao_pagamento=description,
                plano=plano,
                status_pedido='rejected',
                parcelamentos=numero_parcelas,
                IdTransaction=id_transaction,
            )
            
            html_content = render_to_string('email_pagamento_rejeitado.html', {
                'usuario': request.user.username,
                'plano': _plano,
                'description': 'A transação foi devolvida, assim o valor desta retornou para você.',
            })
            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives('Pagamento rejeitado - Cachorrinhas', text_content, 
            settings.EMAIL_HOST_USER, [perfil.email])
            email.attach_alternative(html_content, 'text/html')
            email.send()

            pedido.recebeu_email_reprovado = True
            pedido.save()

            messages.info(request, 'A transação foi devolvida, assim o valor desta retornou para você.')
            return redirect('rejeitado')

        else:
            pedido = Pedido.objects.create(
                comprador=perfil,
                tipo_pagamento='cartao',
                preco_pedido=preco_pedido,
                descricao_pagamento=description,
                plano=plano,
                status_pedido='rejected',
                parcelamentos=numero_parcelas,
                IdTransaction=id_transaction,
            )
            
            html_content = render_to_string('email_pagamento_rejeitado.html', {
                'usuario': request.user.username,
                'plano': _plano,
                'description': 'A transação foi recusada pela operadora do cartão de crédito.',
            })
            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives('Pagamento rejeitado - Cachorrinhas', text_content, 
            settings.EMAIL_HOST_USER, [perfil.email])
            email.attach_alternative(html_content, 'text/html')
            email.send()

            pedido.recebeu_email_reprovado = True
            pedido.save()

            messages.info(request, 'A transação foi recusada pela operadora do cartão de crédito.')
            return redirect('rejeitado')
        

    if not request.user.is_authenticated:
        return redirect('home')

def pagamento_video_premium(request, nome_video):
    http_referer = request.META.get(
		 'HTTP_REFERER',
		 reverse('home')
	)

    if not request.user.is_authenticated:
        return redirect(http_referer)
    
    if not Videos.objects.filter(nome=nome_video, premium=True).exists():
        return redirect(http_referer)
    
    video = Videos.objects.get(nome=nome_video, premium=True)

    if not request.session.get('video_premium'):
        request.session['video_premium'] = {}
    request.session['video_premium'] = video.nome
    request.session['menina'] = video.menina.nome
    request.session.save()

    _nome_video = request.session['video_premium']
    nome_menina = request.session['menina']

    if not Perfil.objects.filter(usuario=request.user).exists():
        perfil = Perfil.objects.create(usuario=request.user, email=request.user.email, nome=request.user.usuario) 
        perfil.save()
    
    perfil = Perfil.objects.get(usuario=request.user)
    preco_pedido = video.preco_premium

    if PedidoVideoPremium.objects.filter(comprador=perfil, video=video, status_pedido='approved').exists():
        return redirect(http_referer)
    
    if request.method != 'POST':
        return render(request, 'area_pagamento_videos.html', {
            'video_premium': _nome_video,
            'preco_pedido': preco_pedido,
        })
    
    tipo_pagamento = request.POST.get('tipo-pagamento')

    if not tipo_pagamento:
        messages.error(request, 'Preencha todos os campos!')
        return render(request, 'area_pagamento_videos.html', {
            'video_premium': _nome_video,
            'preco_pedido': preco_pedido,
        })

    if tipo_pagamento == 'pix':
        url = "https://payment.safe2pay.com.br/v2/Payment"

        payload = {
            "IsSandbox": SANDBOX,
            "Application": f"Cachorrinhas - {video.nome}",
            "Vendor": "Lucas",
            "CallbackUrl": "https://cachorrinha.com.br/perfil/payment_status_video/",
            "PaymentMethod": "6",
            "Reference": f"{perfil.id} -> {video.nome}",
            "Customer": {
                "Name": f"{perfil.usuario.username} -> {perfil.nome}",
                "Identity": "31037942000178", # CPF/CNPJ
                "Email": f"{perfil.email}",
                "Address": {
                    "ZipCode": "90670090",
                    "Street": "Logradouro",
                    "Number": "123",
                    "Complement": "Complemento",
                    "District": "Higienopolis",
                    "CityName": "Porto Alegre",
                    "StateInitials": "RS",
                    "CountryName": "Brasil"
                }
            },
            "Products": [
                {
                    "Code": f"{perfil.id}",
                    "Description": f"{video.nome}",
                    "UnitPrice": preco_pedido,
                    "Quantity": 1,
                },
            ],
        }

        headers = {
            'content-type': "application/json",
            'x-api-key': TOKEN,
        }

        response = requests.post(url, data=json.dumps(payload), headers=headers).json()

        if response.get('HasError'):
            messages.error(request, response.get('Error'))
            return render(request, 'area_pagamento_videos.html', {
                'video_premium': _nome_video,
                'preco_pedido': preco_pedido,
            })
        
        elif response.get('ResponseDetail'):
            try:
                id_transaction = response.get('ResponseDetail').get('IdTransaction')
                message = response.get('ResponseDetail').get('Message')
                description = response.get('ResponseDetail').get('Description')
                status = response.get('ResponseDetail').get('Status')
                link = response.get('ResponseDetail').get('QrCode')
                codigo_pix = response.get('ResponseDetail').get('Key')
            except:
                messages.error(request, 'Ocorreu algum erro com o seu pagamento. Tente novamente!')
                return render(request, 'area_pagamento_videos.html', {
                    'video_premium': _nome_video,
                    'preco_pedido': preco_pedido,
                })
        else:
            messages.error(request, 'Ocorreu algum erro com o seu pagamento. Tente novamente!')
            return render(request, 'area_pagamento_videos.html', {
                'video_premium': _nome_video,
                'preco_pedido': preco_pedido,
            })
        
        if status == '1' or status == 1:

            pedido = PedidoVideoPremium.objects.create(
                comprador=perfil,
                tipo_pagamento='pix',
                preco_pedido=preco_pedido,
                descricao_pagamento=description,
                video=video,
                IdTransaction=id_transaction,
            )
            
            html_content = render_to_string('email_pagamento_pendente_video_pix.html', {
                'usuario': request.user.username,
                'nome_video': _nome_video.replace('-', ' '),
                'codigo_pix': codigo_pix,
                'link': link,
                'description': 'Iniciado uma transação pelo comprador. Por favor, realize o pagamento.'
            })
            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives('Pagamento pendente - Cachorrinhas', text_content, 
            settings.EMAIL_HOST_USER, [perfil.email])
            email.attach_alternative(html_content, 'text/html')
            email.send()

            pedido.recebeu_email_pendente = True
            pedido.save()

            # messages.info(request, 'Por favor, realize o pagamento. Após efetuado, o pagamento pode levar até 5 minutos para ser compensado.')
            # return redirect(f'{DOMINIO}/perfil/premium/{nome_menina}/')

            request.session['codigo_pix'] = codigo_pix
            # request.session['link'] = f'/static/pix/qrcode.png'
            request.session['link'] = link
            request.session.save()
            
            return redirect('pendente_pix')

        elif status == '3' or status == 3:
            pedido = PedidoVideoPremium.objects.create(
                comprador=perfil,
                tipo_pagamento='pix',
                preco_pedido=preco_pedido,
                descricao_pagamento=description,
                video=video,
                IdTransaction=id_transaction,
                status_pedido='approved',
            )

            html_content = render_to_string('email_pagamento_sucesso_video.html', {
                'usuario': request.user.username,
                'nome_video': _nome_video.replace('-', ' '),
                'data_pedido': pedido.data_pedido.strftime('%d/%m/%Y'),
                'link': f'{DOMINIO}/perfil/',
            })
            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives('Pagamento aprovado - Cachorrinhas', text_content, 
            settings.EMAIL_HOST_USER, [perfil.email])
            email.attach_alternative(html_content, 'text/html')
            email.send()

            pedido.recebeu_email_aprovado = True
            pedido.save()

            messages.success(request, 'O seu pagamento foi realizado com sucesso! Video liberado!')
            return redirect(f'{DOMINIO}/perfil/premium/{nome_menina}/')

        else:
            messages.error(request, 'Ocorreu algum erro com o seu pagamento. Tente novamente!')
            return render(request, 'area_pagamento_videos.html', {
                'video_premium': _nome_video,
                'preco_pedido': preco_pedido,
            })

    elif tipo_pagamento == 'cartao':
        nome_cartao = request.POST.get('nome_cartao')
        numero_cartao = request.POST.get('numero_cartao')
        data_expiracao = request.POST.get('data_expiracao')
        numero_parcelas = request.POST.get('numero_parcelas')
        codigo_cartao = request.POST.get('codigo_cartao')

        if not nome_cartao or not numero_cartao or not data_expiracao or not numero_parcelas or not codigo_cartao:
            messages.info(request, f'{request.user.username}, você não tem nenhum plano ativo. Para desfrutar de todo o conteúdo exclusivo, realize o pagamento do plano escolhido.')
            messages.error(request, 'Preencha todos os campos do cartão!')
            return render(request, 'area_pagamento_videos.html', {
                'video_premium': _nome_video,
                'preco_pedido': preco_pedido,
            })
        
        lista = [x for x in data_expiracao]
        lista.insert(3, '20')
        data_expiracao = ''.join(lista)
        
        url = "https://payment.safe2pay.com.br/v2/Payment"

        payload = {
            "IsSandbox": SANDBOX,
            "Application": f"Cachorrinhas - {video.nome}",
            "Vendor": "Lucas",
            "CallbackUrl": "https://www.cachorrinha.com.br/perfil/payment_status_video/",
            "PaymentMethod": "2",
            "Reference": f"{perfil.id} -> {video.nome}",
            "Customer": {
                "Name": f"{perfil.usuario.username} -> {perfil.nome}",
                "Identity": "31037942000178", # CPF/CNPJ
                "Email": f"{perfil.email}",
                "Address": {
                    "ZipCode": "90670090",
                    "Street": "Logradouro",
                    "Number": "123",
                    "Complement": "Complemento",
                    "District": "Higienopolis",
                    "CityName": "Porto Alegre",
                    "StateInitials": "RS",
                    "CountryName": "Brasil"
                }
            },
            "Products": [
                {
                    "Code": f"{perfil.id}",
                    "Description": f"{video.nome}",
                    "UnitPrice": preco_pedido,
                    "Quantity": 1,
                },
            ],
            "PaymentObject": {
                "Holder": nome_cartao,
                "CardNumber": numero_cartao,
                "ExpirationDate": f'{data_expiracao}',
                "SecurityCode": f'{codigo_cartao}',
                "InstallmentQuantity": numero_parcelas,
            }
        }

        headers = {
            'content-type': "application/json",
            'x-api-key': TOKEN,
        }

        response = requests.post(url, data=json.dumps(payload), headers=headers).json()


        if response.get('HasError'):
            messages.error(request, response.get('Error'))
            return render(request, 'area_pagamento_videos.html', {
                'video_premium': _nome_video,
                'preco_pedido': preco_pedido,
            })
        elif response.get('ResponseDetail'):
            try:
                id_transaction = response.get('ResponseDetail').get('IdTransaction')
                message = response.get('ResponseDetail').get('Message')
                description = response.get('ResponseDetail').get('Description')
                status = response.get('ResponseDetail').get('Status')
            except:
                messages.error(request, 'Ocorreu algum erro com o seu pagamento. Tente novamente!')
                return render(request, 'area_pagamento_videos.html', {
                    'video_premium': _nome_video,
                    'preco_pedido': preco_pedido,
                })
        else:
            messages.error(request, 'Ocorreu algum erro com o seu pagamento. Tente novamente!')
            return render(request, 'area_pagamento_videos.html', {
                'video_premium': _nome_video,
                'preco_pedido': preco_pedido,
            })

    
        if status == '3' or status == 3:
            pedido = PedidoVideoPremium.objects.create(
                comprador=perfil,
                tipo_pagamento='cartao',
                preco_pedido=preco_pedido,
                descricao_pagamento=description,
                video=video,
                parcelamentos=numero_parcelas,
                IdTransaction=id_transaction,
                status_pedido='approved',
            )

            html_content = render_to_string('email_pagamento_sucesso_video.html', {
                'usuario': request.user.username,
                'nome_video': _nome_video.replace('-', ' '),
                'data_pedido': pedido.data_pedido.strftime('%d/%m/%Y'),
                'link': f'{DOMINIO}/perfil/',
            })
            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives('Pagamento aprovado - Cachorrinhas', text_content, 
            settings.EMAIL_HOST_USER, [perfil.email])
            email.attach_alternative(html_content, 'text/html')
            email.send()

            pedido.recebeu_email_aprovado = True
            pedido.save()

            messages.success(request, 'O seu pagamento foi realizado com sucesso! Video liberado!')
            return redirect(f'{DOMINIO}/perfil/premium/{nome_menina}/')

        if status == '5' or status == 5:

            pedido = PedidoVideoPremium.objects.create(
                comprador=perfil,
                tipo_pagamento='cartao',
                preco_pedido=preco_pedido,
                descricao_pagamento=description,
                video=video,
                parcelamentos=numero_parcelas,
                IdTransaction=id_transaction,
            )
            
            html_content = render_to_string('email_pagamento_pendente_video.html', {
                'usuario': request.user.username,
                'nome_video': _nome_video.replace('-', ' '),
                'description': 'Dentro do prazo de liberação da transação, você abriu uma disputa para fins de contestação da transação.',
            })
            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives('Pagamento pendente - Cachorrinhas', text_content, 
            settings.EMAIL_HOST_USER, [perfil.email])
            email.attach_alternative(html_content, 'text/html')
            email.send()

            pedido.recebeu_email_pendente = True
            pedido.save()

            messages.info(request, 'Por favor, realize o pagamento. Após efetuado, o pagamento pode levar até 5 minutos para ser compensado.')
            return redirect(f'{DOMINIO}/perfil/premium/{nome_menina}/')
        
        if status == '6' or status == 6:

            pedido = PedidoVideoPremium.objects.create(
                comprador=perfil,
                tipo_pagamento='cartao',
                preco_pedido=preco_pedido,
                descricao_pagamento=description,
                video=video,
                status_pedido='rejected',
                parcelamentos=numero_parcelas,
                IdTransaction=id_transaction,
            )
            
            html_content = render_to_string('email_pagamento_rejeitado_video.html', {
                'usuario': request.user.username,
                'nome_video': _nome_video.replace('-', ' '),
                'description': 'A transação foi devolvida, assim o valor desta retornou para você.',
            })
            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives('Pagamento rejeitado - Cachorrinhas', text_content, 
            settings.EMAIL_HOST_USER, [perfil.email])
            email.attach_alternative(html_content, 'text/html')
            email.send()

            pedido.recebeu_email_reprovado = True
            pedido.save()

            messages.info(request, 'A transação foi devolvida, assim o valor desta retornou para você.')
            return redirect(f'{DOMINIO}/perfil/premium/{nome_menina}/')

        else:
            pedido = PedidoVideoPremium.objects.create(
                comprador=perfil,
                tipo_pagamento='cartao',
                preco_pedido=preco_pedido,
                descricao_pagamento=description,
                video=video,
                status_pedido='rejected',
                parcelamentos=numero_parcelas,
                IdTransaction=id_transaction,
            )
            
            html_content = render_to_string('email_pagamento_rejeitado_video.html', {
                'usuario': request.user.username,
                'nome_video': _nome_video,
                'description': 'A transação foi recusada pela operadora do cartão de crédito.',
            })
            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives('Pagamento rejeitado - Cachorrinhas', text_content, 
            settings.EMAIL_HOST_USER, [perfil.email])
            email.attach_alternative(html_content, 'text/html')
            email.send()

            pedido.recebeu_email_reprovado = True
            pedido.save()

            messages.info(request, 'A transação foi devolvida, assim o valor desta retornou para você.')
            return redirect(f'{DOMINIO}/perfil/premium/{nome_menina}/')
        
    if not request.user.is_authenticated:
        return redirect('home')


@csrf_exempt
def payment_status(request):
    payload = json.loads(request.body.decode('utf-8'))

    if payload.get('IdTransaction') and payload.get('TransactionStatus') and payload['TransactionStatus'].get('Name') and payload.get('PaymentMethod') and payload['PaymentMethod'].get('Name'):
        id_transaction = payload.get('IdTransaction')
        situation = payload.get('TransactionStatus').get('Name')
        payment_method = payload.get('PaymentMethod').get('Name')

        if not Pedido.objects.filter(IdTransaction=id_transaction).exists():
            return HttpResponse('')
        
        pedido = Pedido.objects.get(IdTransaction=id_transaction)
        plano = pedido.plano
        _plano = plano.replace('_', ' ').capitalize().replace('Tres', 'Três')

        if situation == 'Autorizado':
            if plano == 'tres_meses':
                data_validade = pedido.data_pedido + relativedelta(months=3)
            elif plano == 'seis_meses':
                data_validade = pedido.data_pedido + relativedelta(months=6)
            else:
                data_validade = pedido.data_pedido + relativedelta(months=1)
            
            pedido.data_vencimento = data_validade

            pedido.status_pedido = 'approved'
            pedido.plano_ativo = True
            pedido.save()

            if not pedido.recebeu_email_aprovado:
                html_content = render_to_string('email_pagamento_sucesso.html', {
                    'usuario': pedido.comprador.usuario.username,
                    'plano': _plano,
                    'data_pedido': pedido.data_pedido.strftime('%d/%m/%Y'),
                    'data_validade': pedido.data_vencimento.strftime('%d/%m/%Y'),
                    'link': f'{DOMINIO}/perfil/',
                })
                text_content = strip_tags(html_content)

                email = EmailMultiAlternatives('Pagamento aprovado - Cachorrinhas', text_content, 
                settings.EMAIL_HOST_USER, [pedido.comprador.email])
                email.attach_alternative(html_content, 'text/html')
                email.send()

                pedido.recebeu_email_aprovado = True
                pedido.save()
        
        elif situation == 'Devolvido':   
            if not pedido.recebeu_email_reprovado:
                html_content = render_to_string('email_pagamento_rejeitado.html', {
                    'usuario': request.user.username,
                    'plano': _plano,
                    'description': 'A transação foi devolvida, assim o valor desta retornou para você.',
                })
                text_content = strip_tags(html_content)

                email = EmailMultiAlternatives('Pagamento rejeitado - Cachorrinhas', text_content, 
                settings.EMAIL_HOST_USER, [pedido.comprador.email])
                email.attach_alternative(html_content, 'text/html')
                email.send()

                pedido.recebeu_email_reprovado = True
                pedido.save()

    return HttpResponse('')


@csrf_exempt
def payment_status_video(request):
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except:
        return HttpResponse('')

    if payload.get('IdTransaction') and payload.get('TransactionStatus') and payload['TransactionStatus'].get('Name') and payload.get('PaymentMethod') and payload['PaymentMethod'].get('Name'):
        id_transaction = payload.get('IdTransaction')
        situation = payload.get('TransactionStatus').get('Name')
        payment_method = payload.get('PaymentMethod').get('Name')

        if not PedidoVideoPremium.objects.filter(IdTransaction=id_transaction).exists():
            return HttpResponse('')
        
        pedido = PedidoVideoPremium.objects.get(IdTransaction=id_transaction)
        video = pedido.video

        if situation == 'Autorizado':
            pedido.status_pedido = 'approved'
            pedido.save()

            if not pedido.recebeu_email_aprovado:
                html_content = render_to_string('email_pagamento_sucesso_video.html', {
                    'usuario': pedido.comprador.usuario.username,
                    'nome_video': video.nome.replace('-', ' '),
                    'data_pedido': pedido.data_pedido.strftime('%d/%m/%Y'),
                    'link': f'{DOMINIO}/perfil/',
                })
                text_content = strip_tags(html_content)

                email = EmailMultiAlternatives('Pagamento aprovado - Cachorrinhas', text_content, 
                settings.EMAIL_HOST_USER, [pedido.comprador.email])
                email.attach_alternative(html_content, 'text/html')
                email.send()

                pedido.recebeu_email_aprovado = True
                pedido.save()
        
        elif situation == 'Devolvido':   
            if not pedido.recebeu_email_reprovado:
                html_content = render_to_string('email_pagamento_rejeitado_video.html', {
                    'usuario': pedido.comprador.usuario.username,
                    'nome_video': video.nome.replace('-', ' '),
                    'description': 'A transação foi devolvida, assim o valor desta retornou para você.',
                })
                text_content = strip_tags(html_content)

                email = EmailMultiAlternatives('Pagamento rejeitado - Cachorrinhas', text_content, 
                settings.EMAIL_HOST_USER, [pedido.comprador.email])
                email.attach_alternative(html_content, 'text/html')
                email.send()

                pedido.recebeu_email_reprovado = True
                pedido.save()

    return HttpResponse('')


def sucesso(request):
    return render(request, 'sucesso.html')

def rejeitado(request):
    return render(request, 'rejeitado.html')

def pendente(request):
    return render(request, 'pendente.html')

def pendente_pix(request):
    return render(request, 'pendente_pix.html')


def meus_dados(request):
    if not request.user.is_authenticated:
        return redirect('home')

    if not Perfil.objects.filter(usuario=request.user).exists():
        perfil = Perfil.objects.create(usuario=request.user, email=request.user.email, nome=request.user.usuario) 
        perfil.save()
    
    perfil = Perfil.objects.get(usuario=request.user)
    validador = False

    if Pedido.objects.filter(comprador=perfil).exists():
        pedido = Pedido.objects.filter(comprador=perfil).order_by('-data_pedido').first()
        validador = verificacao_planos(pedido)

        plano = pedido.plano.capitalize().replace('_', ' ').replace('Tres', 'Três')
        status_pedido = pedido.status_pedido

        data_pedido = pedido.data_pedido
        data_validade = pedido.data_vencimento

        if status_pedido == 'approved':
            status_pedido = 'Aprovado'
        elif status_pedido == 'rejected':
            status_pedido = 'Rejeitado'
        else:
            status_pedido = 'Pendente'

        if data_validade:
            data_validade = data_validade.strftime('%d/%m/%Y')
        data_pedido = data_pedido.strftime('%d/%m/%Y')

        return render(request, 'meus_dados.html', {
            'validador': validador,
            'pedido': pedido,
            'plano': plano,
            'status_pedido': status_pedido,
            'data_pedido': data_pedido,
            'data_validade': data_validade,
            'perfil': perfil,
        })

    else:
        return render(request, 'meus_dados.html', {
            'validador': validador,
            'perfil': perfil,
        })


def pagina_video(request, nome_video):
    ############

    if not request.user.is_authenticated:
        return redirect('home')
    
    if not Perfil.objects.filter(usuario=request.user).exists():
        perfil = Perfil.objects.create(usuario=request.user, email=request.user.email, nome=request.user.usuario) 
        perfil.save()
    
    perfil = Perfil.objects.get(usuario=request.user)

    if Pedido.objects.filter(comprador=perfil, plano_ativo=True, status_pedido='approved').exists():
        pedido = Pedido.objects.filter(comprador=perfil, plano_ativo=True, status_pedido='approved').first()
        validador = verificacao_planos(pedido)
        if not validador:
            messages.error(request, 'Infelizmente, o período do seu plano chegou ao fim. Para continuar desfrutando de todo o conteúdo exclusivo por mais tempo, recomendamos que você renove seu plano.')
            return redirect('area_pagamento')
    else:
        return redirect('area_pagamento')
    
    ############

    if not Videos.objects.filter(nome=nome_video).exists():
        raise Http404

    video = Videos.objects.get(nome=nome_video)
    # perfil = Perfil.objects.all().first()

    comentarios = Comentarios.objects.filter(video__nome=nome_video, visibilidade=True)

    if len(comentarios) == 0:
        numero_curtidas = 5
    else:
        numero_curtidas = len(comentarios) + len(comentarios) * 3

    if request.method != 'POST':
        return render(request, 'pagina_video.html', {
            'video': video,
            'menina': video.menina,
            'comentarios': comentarios,
            'numero_comentarios': len(comentarios),
            'numero_curtidas': numero_curtidas,
        })
    
    texto = request.POST.get('texto')
    comentario = Comentarios.objects.create(perfil=perfil, comentario=texto, video=video)
    comentario.save()

    messages.success(request, 'O seu comentário foi registrado com sucesso. Aguarde a aprovação do seu comentário pelo administrador.')
    return render(request, 'pagina_video.html', {
        'video': video,
        'menina': video.menina,
        'comentarios': comentarios,
        'numero_comentarios': len(comentarios),
        'numero_curtidas': numero_curtidas,
    })



def videos(request):
    ###################
    if not request.user.is_authenticated:
        return redirect('home')
    
    if not Perfil.objects.filter(usuario=request.user).exists():
        perfil = Perfil.objects.create(usuario=request.user, email=request.user.email, nome=request.user.usuario) 
        perfil.save()
    
    perfil = Perfil.objects.get(usuario=request.user)

    if Pedido.objects.filter(comprador=perfil, plano_ativo=True, status_pedido='approved').exists():
        pedido = Pedido.objects.filter(comprador=perfil, plano_ativo=True, status_pedido='approved').first()
        validador = verificacao_planos(pedido)
        if not validador:
            messages.error(request, 'Infelizmente, o período do seu plano chegou ao fim. Para continuar desfrutando de todo o conteúdo exclusivo por mais tempo, recomendamos que você renove seu plano.')
            return redirect('meus_dados')
    else:
        return redirect('area_pagamento')
    #####################

    meninas = Meninas.objects.all()
    # videos = Videos.objects.filter(premium=False)
    videos = Videos.objects.all()

    lista_validador = []

    """ for video in videos:
        if video.premium:
            ...
        else:
            ... """

    for video in videos:
        if PedidoVideoPremium.objects.filter(video=video, comprador=perfil, status_pedido='approved').exists():
            lista_validador.append(True)
        else:
            lista_validador.append(False)

    lista_zip = list(zip(list(videos), lista_validador))

    return render(request, 'videos.html', {
        'meninas': meninas,
        'lista_zip': lista_zip,
    })

def perfil_videos(request, nome_menina):
    ############
    if not request.user.is_authenticated:
        return redirect('home')
    
    if not Perfil.objects.filter(usuario=request.user).exists():
        perfil = Perfil.objects.create(usuario=request.user, email=request.user.email, nome=request.user.usuario) 
        perfil.save()
    
    perfil = Perfil.objects.get(usuario=request.user)

    if Pedido.objects.filter(comprador=perfil, plano_ativo=True, status_pedido='approved').exists():
        pedido = Pedido.objects.filter(comprador=perfil, plano_ativo=True, status_pedido='approved').first()
        validador = verificacao_planos(pedido)
        if not validador:
            messages.error(request, 'Infelizmente, o período do seu plano chegou ao fim. Para continuar desfrutando de todo o conteúdo exclusivo por mais tempo, recomendamos que você renove seu plano.')
            return redirect('meus_dados')
    else:
        return redirect('meus_dados')
    ############

    if not Meninas.objects.filter(nome=nome_menina).exists():
        return redirect('videos')

    menina = Meninas.objects.get(nome=nome_menina)

    if not Videos.objects.filter(menina=menina, premium=False).exists():
        return redirect(f'{DOMINIO}/perfil/premium/{nome_menina}/')
    
    videos = Videos.objects.filter(menina=menina, premium=False)

    return render(request, 'perfil_videos.html', {
        'menina': menina,
        'videos': videos,
    })

def perfil_premium(request, nome_menina):
   ############
    if not request.user.is_authenticated:
        return redirect('home')
    
    if not Perfil.objects.filter(usuario=request.user).exists():
        perfil = Perfil.objects.create(usuario=request.user, email=request.user.email, nome=request.user.usuario) 
        perfil.save()
    
    perfil = Perfil.objects.get(usuario=request.user)

    if Pedido.objects.filter(comprador=perfil, plano_ativo=True, status_pedido='approved').exists():
        pedido = Pedido.objects.filter(comprador=perfil, plano_ativo=True, status_pedido='approved').first()
        validador = verificacao_planos(pedido)
        if not validador:
            messages.error(request, 'Infelizmente, o período do seu plano chegou ao fim. Para continuar desfrutando de todo o conteúdo exclusivo por mais tempo, recomendamos que você renove seu plano.')
            return redirect('meus_dados')
    else:
        return redirect('meus_dados')
    ############

    if not Meninas.objects.filter(nome=nome_menina).exists():
        return redirect('videos')

    menina = Meninas.objects.get(nome=nome_menina)

    if not Videos.objects.filter(menina=menina, premium=True).exists():
        return redirect(f'{DOMINIO}/perfil/audios/{nome_menina}/')
    
    videos = Videos.objects.filter(menina=menina, premium=True)
    lista_validador = []

    for video in videos:
        if PedidoVideoPremium.objects.filter(video=video, comprador=perfil, status_pedido='approved').exists():
            lista_validador.append(True)
        else:
            lista_validador.append(False)

    lista_zip = list(zip(list(videos), lista_validador))

    return render(request, 'perfil_premium.html', {
        'menina': menina,
        'lista_zip': lista_zip,
    })

def perfil_audios(request, nome_menina):
    ############
    if not request.user.is_authenticated:
        return redirect('home')
    
    if not Perfil.objects.filter(usuario=request.user).exists():
        perfil = Perfil.objects.create(usuario=request.user, email=request.user.email, nome=request.user.usuario) 
        perfil.save()
    
    perfil = Perfil.objects.get(usuario=request.user)

    if Pedido.objects.filter(comprador=perfil, plano_ativo=True, status_pedido='approved').exists():
        pedido = Pedido.objects.filter(comprador=perfil, plano_ativo=True, status_pedido='approved').first()
        validador = verificacao_planos(pedido)
        if not validador:
            messages.error(request, 'Infelizmente, o período do seu plano chegou ao fim. Para continuar desfrutando de todo o conteúdo exclusivo por mais tempo, recomendamos que você renove seu plano.')
            return redirect('meus_dados')
    else:
        return redirect('meus_dados')
    ############

    if not Meninas.objects.filter(nome=nome_menina).exists():
        return redirect('videos')

    menina = Meninas.objects.get(nome=nome_menina)

    if not Audios.objects.filter(menina=menina).exists():
        return redirect('videos')
    
    audios = Audios.objects.filter(menina=menina)

    try:
        audio1 = audios[0]
    except:
        audio1 = None

    try:
        audio2 = audios[1]
    except:
        audio2 = None

    try:
        audio3 = audios[2]
    except:
        audio3 = None

    try:
        audio4 = audios[3]
    except:
        audio4 = None

    return render(request, 'perfil_audios.html', {
        'menina': menina,
        'audio1': audio1,
        'audio2': audio2,
        'audio3': audio3,
        'audio4': audio4,
    })


def editar_perfil(request):
    if not request.user.is_authenticated:
        return redirect('home')

    if request.method != 'POST':
        return render(request, 'editar_perfil.html')

    if not Perfil.objects.filter(usuario=request.user).exists():
        messages.error(request, 'Seu usuário não está atrelado a nenhum perfil. Fale com o suporte!')
        return render(request, 'editar_perfil.html')

    nome = request.POST.get('nome')
    usuario = request.POST.get('usuario')
    email = request.POST.get('email')

    if not email or not nome:
        messages.error(request, 'Nenhum campo pode ficar vazio!')
        return render(request, 'editar_perfil.html')
    
    if len(nome) >= 60:
        messages.error(request, 'Digite um nome com 30 caracteres ou menos!')
        return render(request, 'editar_perfil.html')
    
    if len(usuario) > 8:
        messages.error(request, 'Digite um usuário com 8 caracteres ou menos!')
        return render(request, 'editar_perfil.html')

    try:
        validate_email(email)
    except:
        messages.error(request, 'E-mail inválido!')
        return render(request, 'editar_perfil.html')
    
    """ link = f'https://api.usebouncer.com/v1/email/verify?email={email}&timeout=10'
    headers = {
        "Accept": "application/json",
        'x-api-key': KEY_API_USEBOUNCER,
    }
    requisicao = requests.get(link, headers=headers)

    if str(requisicao) != '<Response [200]>':
        messages.error(request, 'No momento não foi possível criar a sua conta. Tente novamente mais tarde!')
        return render(request, 'editar_perfil.html')
    
    status = dict(requisicao.json())['reason']
    if status != 'accepted_email':
        messages.error(request, 'O E-mail informado NÃO existe!')
        return render(request, 'editar_perfil.html') """
    
    if User.objects.filter(email=email).exists() or Perfil.objects.filter(email=email).exists():
        messages.error(request, 'O E-mail informado já está sendo utilizado!')
        return render(request, 'editar_perfil.html')
    
    if User.objects.filter(username=usuario).exists():
        messages.error(request, 'O usuário informado já está sendo utilizado!')
        return render(request, 'editar_perfil.html')

    messages.success(request, 'Editado com sucesso!')

    perfil = Perfil.objects.get(usuario=request.user)
    user = User.objects.get(username=request.user.username)
    user.email = email
    user.username = usuario
    user.save()
    perfil.nome = nome
    perfil.email = email
    perfil.save()

    return redirect('meus_dados')


def esqueceu_senha(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method != 'POST':
        return render(request, 'esqueceu_senha.html')

    email = request.POST.get('email')

    if not email:
        messages.error(request, 'Digite o seu e-mail!')
        return render(request, 'esqueceu_senha.html')
    
    if not User.objects.filter(email=email).exists():
        messages.error(request, 'O e-mail enviado não está atrelado a nenhuma conta!')
        return render(request, 'esqueceu_senha.html')
    
    usuario = User.objects.get(email=email)

    if not Perfil.objects.filter(usuario=usuario).exists():
        messages.error(request, 'Seu usuário não está atrelado a nenhum perfil. Fale com o suporte!')
        return render(request, 'esqueceu_senha.html')
    perfil = Perfil.objects.get(usuario=usuario)

    if not request.session.get('secret'):
        request.session['secret'] = {}
    secret = request.session['secret']

    letras = string.ascii_letters
    digitos = string.digits
    # caracteres = string.punctuation

    geral = letras + digitos
    codigo = ''.join(random.choices(geral, k=25))
    secret['trocar_senha_codigo'] = codigo
    link = f'{DOMINIO}/perfil/formulario_esqueceu_senha/{codigo}'
    secret['trocar_senha_link'] = link
    secret['trocar_senha_usuario'] = usuario.username
    request.session.save()

    html_content = render_to_string('email_recuperacao_senha.html', {'link': link})
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives('Redefinir senha - Cachorrinhas', text_content, 
    settings.EMAIL_HOST_USER, [email])
    email.attach_alternative(html_content, 'text/html')
    email.send()

    messages.success(request, 'Digite seu e-mail e acesse o link para que você possa alterar sua senha!')
    return render(request, 'esqueceu_senha.html')


def formulario_esqueceu_senha(request, codigo):
    if request.user.is_authenticated:
        return redirect('home')

    if not request.session.get('secret'):
        return redirect('home')
    
    secret = request.session['secret']

    trocar_senha_codigo = secret['trocar_senha_codigo']
    trocar_senha_usuario = secret['trocar_senha_usuario']

    if trocar_senha_codigo != codigo:
        return redirect('home')

    if not User.objects.filter(username=trocar_senha_usuario).exists():
        messages.error(request, f"O usuário: '{trocar_senha_usuario}' não existe mais!")
        return render(request, 'trocar_senha.html')

    if request.method != 'POST':
        return render(request, 'trocar_senha.html')
    
    senha1 = request.POST.get('senha1')
    senha2 = request.POST.get('senha2')

    if not senha1 or not senha2:
        messages.error(request, 'Os campos não podem ficar vazios!')
        return render(request, 'trocar_senha.html')

    if len(senha1) < 4:
        messages.error(request, 'A senha não pode ter menos que 4 caracteres!')
        return render(request, 'trocar_senha.html')

    if senha1 != senha2:
        messages.error(request, 'As senhas precisam ser iguais!')
        return render(request, 'trocar_senha.html')

    del request.session['secret']
    request.session.save()
    
    user = User.objects.get(username=trocar_senha_usuario)

    user.set_password(senha1)
    auth.logout(request)
    user.save()
    
    messages.success(request, f'Olá {user}, a sua senha foi trocada!')
    return redirect('login')


