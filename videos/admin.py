from django.contrib import admin
from .models import Pedido, Videos, Comentarios, Planos, Audios, PedidoVideoPremium

class VideosAdmin(admin.ModelAdmin):
	list_display = ('id', 'link', 'nome', 'descricao', 'premium', 'menina')
	list_display_links = ('id', 'link', 'nome', 'descricao', 'premium', 'menina')
	list_filter = ('premium', 'menina')
	list_per_page = 10
	search_fields = ('nome', 'descricao')

admin.site.register(Videos, VideosAdmin)

class AudiosAdmin(admin.ModelAdmin):
	list_display = ('id', 'menina', 'nome', 'arquivo')
	list_display_links = ('id', 'menina', 'nome', 'arquivo')
	list_filter = ('menina',)
	list_per_page = 10
	search_fields = ('nome',)

admin.site.register(Audios, AudiosAdmin)

class PlanosAdmin(admin.ModelAdmin):
	list_display = ('id', 'tres_meses', 'seis_meses', 'um_mes')
	list_display_links = ('id', 'tres_meses', 'seis_meses', 'um_mes')
	list_per_page = 10

admin.site.register(Planos, PlanosAdmin)

class ComentariosAdmin(admin.ModelAdmin):
	list_display = ('id', 'perfil', 'comentario', 'video', 'visibilidade')
	list_display_links = ('id', 'perfil', 'comentario', 'video')
	list_filter = ('video',)
	list_editable = ('visibilidade',)
	list_per_page = 10
	search_fields = ('perfil__nome', 'comentario')


admin.site.register(Comentarios, ComentariosAdmin)

class PedidoAdmin(admin.ModelAdmin):
	list_display = ('id', 'comprador', 'tipo_pagamento', 'preco_pedido', 'data_pedido', 'status_pedido', 'plano', 'plano_ativo')
	list_display_links = ('id', 'comprador', 'tipo_pagamento', 'preco_pedido', 'data_pedido', 'status_pedido', 'plano')
	list_filter = ('status_pedido', 'plano', 'plano_ativo')
	list_per_page = 10
	search_fields = ('comprador__nome', 'tipo_pagamento', 'preco_pedido')

admin.site.register(Pedido, PedidoAdmin)

class PedidoVideoPremiumAdmin(admin.ModelAdmin):
	list_display = ('id', 'comprador', 'tipo_pagamento', 'preco_pedido', 'data_pedido', 'status_pedido', 'video')
	list_display_links = ('id', 'comprador', 'tipo_pagamento', 'preco_pedido', 'data_pedido', 'status_pedido', 'video')
	list_filter = ('status_pedido', 'video')
	list_per_page = 10
	search_fields = ('comprador__nome', 'tipo_pagamento', 'preco_pedido')

admin.site.register(PedidoVideoPremium, PedidoVideoPremiumAdmin)
