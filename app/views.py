from django.shortcuts import render
from app import populateDB
from app import whooshIndex
from .models import Colection, Game, Mod
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from .forms import ModBusquedaForm,ColBusquedaForm

def index(request):
    return render(request, 'app/index.html')

@login_required(login_url='/ingresar')
def cargarDatos(request):
    if populateDB.populate():
        gam = Game.objects.all().count()
        col = Colection.objects.all().count()
        mod = Mod.objects.all().count()
        informacion="Datos cargados correctamente\n" + "Juegos: " + str(gam) + ", "+"Colecciones: "+str(col)+", " + " \n Mods: " + str(mod)  
    else:
        informacion="ERROR en la carga de datos"
    whooshIndex.crearIndex()
    
    logout(request)    
    return render(request, 'app/populate.html', {'inf':informacion})

def crearIndex(request):
    whooshIndex.crearIndex()
    return render(request, 'app/index.html')

def ingresar(request):
    formulario = AuthenticationForm()
    if request.method=='POST':
        formulario = AuthenticationForm(request.POST)
        usuario=request.POST['username']
        clave=request.POST['password']
        acceso=authenticate(username=usuario,password=clave)
        if acceso is not None:
            if acceso.is_active:
                login(request, acceso)
                return (HttpResponseRedirect('/cargar'))
            else:
                return render(request, 'app/mensaje_error.html',{'error':"USUARIO NO ACTIVO",'STATIC_URL':settings.STATIC_URL})
        else:
            return render(request, 'app/mensaje_error.html',{'error':"USUARIO O CONTRASEÑA INCORRECTOS",'STATIC_URL':settings.STATIC_URL})
                     
    return render(request, 'app/ingresar.html', {'formulario':formulario, 'STATIC_URL':settings.STATIC_URL})


def lista_juegos(request):
    juegos=Game.objects.all()
    return render(request,'app/juegos.html', {'datos':juegos})

def detalle_juego(request, id_game):
    juego = get_object_or_404(Game, pk=id_game)
    return render(request,'app/juego.html',{'juego':juego})

def get_mod(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ModBusquedaForm(request.POST)
        mod = request.POST['mod']
        results = whooshIndex.buscarMods(mod)
        if form.is_valid():
            
            return render(request, 'app/busquedasMods.html', {'mods': results})
    else:
        form = ModBusquedaForm()

    return render(request, 'app/modsQuery.html', {'form': form})

def get_col(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ColBusquedaForm(request.POST)
        col = request.POST['col']
        results = whooshIndex.buscarMods(col)
        if form.is_valid():
            
            return render(request, 'app/busquedasCols.html', {'cols': results})
    else:
        form = ColBusquedaForm()

    return render(request, 'app/colsQuery.html', {'form': form})

class lista_mods(ListView):
    model = Mod
    template_name = 'app/mods.html' 
    paginate_by = 10
    context_object_name = 'mods'

class lista_colecciones(ListView):
    model = Colection
    template_name = 'app/colections.html' 
    paginate_by = 10
    context_object_name = 'colections'


    