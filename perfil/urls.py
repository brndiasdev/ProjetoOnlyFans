from django.urls import path
from . import views

urlpatterns = [
    path('', views.videos, name='videos'),
    path('pagina_video/<slug:nome_video>/', views.pagina_video, name='pagina_video'),
    path('perfil_menina/<str:nome_menina>/', views.perfil_videos, name='perfil_videos'),
    path('premium/<str:nome_menina>/', views.perfil_premium, name='perfil_premium'),
    path('audios/<str:nome_menina>/', views.perfil_audios, name='perfil_audios'),

    path('login/', views.login, name='login'),
    path('registro/', views.registro, name='registro'),
    path('logout/', views.logout, name='logout'),

    path('verificacao_planos/', views.verificacao_planos, name='verificacao_planos'),
    path('area_pagamento/', views.area_pagamento, name='area_pagamento'),
    path('pagamento_video_premium/<slug:nome_video>/', views.pagamento_video_premium, name='pagamento_video_premium'),

    path('sucesso/', views.sucesso, name='sucesso'),
    path('rejeitado/', views.rejeitado, name='rejeitado'),
    path('pendente/', views.pendente, name='pendente'),
    path('pendente_pix/', views.pendente_pix, name='pendente_pix'),

    path('payment_status/', views.payment_status, name='payment_status'),
    path('payment_status_video/', views.payment_status_video, name='payment_status_video'),

    path('meus_dados/', views.meus_dados, name='meus_dados'),

    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),
    path('esqueceu_senha/', views.esqueceu_senha, name='esqueceu_senha'),
    path('formulario_esqueceu_senha/<str:codigo>/', views.formulario_esqueceu_senha, name='formulario_esqueceu_senha'),
]