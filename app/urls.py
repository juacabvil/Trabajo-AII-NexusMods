"""nexusmods URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app import views
from app import populateDB

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('cargar/', views.cargarDatos, name='cargar'),
    path('ingresar/', views.ingresar), 
    path('juegos/',views.lista_juegos),
    path('juegos/<int:id_game>', views.detalle_juego),
    path('mods/', view=views.lista_mods.as_view()),
    path('colections/', view=views.lista_colecciones.as_view()),
    path('loadindex/',views.crearIndex),
    path('buscarMod/',views.get_mod),
    path('buscarCol/',views.get_col),


]

