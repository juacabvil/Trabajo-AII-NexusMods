from django.shortcuts import render
from app import populateDB

def index(request):
    return render(request, 'app/index.html')

def cargarIndex(request):
    populateDB.extraer_juegos()
    return render(request, 'app/index.html')

