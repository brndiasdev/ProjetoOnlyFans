from django.contrib import admin
from .models import Perfil, Meninas

class PerfilAdmin(admin.ModelAdmin):
	list_display = ('id', 'usuario', 'nome', 'email')
	list_display_links = ('id', 'usuario', 'nome', 'email')
	list_per_page = 10
	search_fields = ('usuario__username', 'nome', 'email')


admin.site.register(Perfil, PerfilAdmin)

class MeninasAdmin(admin.ModelAdmin):
	list_display = ('id', 'nome', 'email')
	list_display_links = ('id', 'nome', 'email')
	list_per_page = 10
	search_fields = ('nome', 'email')


admin.site.register(Meninas, MeninasAdmin)
