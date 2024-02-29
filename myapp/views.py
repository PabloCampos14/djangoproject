from django.shortcuts import render
from django.http import HttpResponse 
from django.template import Template, Context
from .forms import ReclasificadorForm

# Create your views here.
def hello (request):
    #creación de una instancia del formulario ReclasificadorForm
    form = ReclasificadorForm(request.POST or None)

    #Logica para procesar el formulario cuando se envia 
    if request.method == 'POST' and form.is_valid():
        #Obtiene elementos seleccionados de los campos del formulario
        elementos_izquierda = form.cleaned_data['elementos_izquierda']
        elementos_derecha = form.cleaned_data['elementos_derecha']

    
    #NOTA: Falta la lógica para mover elementos entre listas o cualquier otra acción
    #ADEMÁS agregar la base de datos para comenzar las pruebas en SQL server
        
    
    return render(request, 'misplantillas.html', {'form': form})

def prueba (request):
    #Temporalmente vacío en lo que se me ocurre que poner en esta extensión xd
    return render(request, 'index.html')

