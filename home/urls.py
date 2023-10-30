from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('escolher_plano/<str:plano>/', views.escolher_plano, name='escolher_plano'),
]