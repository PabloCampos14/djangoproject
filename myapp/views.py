from django.shortcuts import render
from django.http import HttpResponse 
from django.template import Template, Context
from .forms import ReclasificadorForm
import pyodbc

# Create your views here.

def hello (request):
    #creación de una instancia del formulario ReclasificadorForm
    form = ReclasificadorForm(request.POST or None)

    conn = pyodbc.connect('Driver={sql server};'
                      'Server=gsvwdb17\sql2014;'
                      'Database=Pruebas3;'
                      'UID=gsvreportes;'
                      'PWD=Ind2019&;'
                      'Trusted_Connection=no;')
    cursor = conn.cursor()
    cursor.execute("select * from zClasifProveedores")
    result = cursor.fetchall()

    #Logica para procesar el formulario cuando se envia 
    if request.method == 'POST' and form.is_valid():
        #Obtiene elementos seleccionados de los campos del formulario
        elementos_izquierda = form.cleaned_data['elementos_izquierda']
        elementos_derecha = form.cleaned_data['elementos_derecha']

    
    #NOTA: Falta la lógica para mover elementos entre listas o cualquier otra acción
    #ADEMÁS agregar la base de datos para comenzar las pruebas en SQL server
        
    
    return render(request, 'misplantillas.html', {'clasf_Proveedor_Tabla': result})

def tabla(request):
    conn = pyodbc.connect('Driver={sql server};'
                      'Server=gsvwdb17\sql2014;'
                      'Database=Pruebas3;'
                      'UID=gsvreportes;'
                      'PWD=Ind2019&;'
                      'Trusted_Connection=no;')
    cursor = conn.cursor()
    cursor.execute("select * from zClasifProveedores")
    result = cursor.fetchall()
    return render(request, 'Tabla.html', {'clasf_Proveedor_Tabla': result})
#ORM https://stackoverflow.com/questions/372885/how-do-i-connect-to-a-mysql-database-in-python/622308#622308


def prueba (request):
    #Temporalmente vacío en lo que se me ocurre que poner en esta extensión xd
    #Me equivoqué la tabla de la base de datos se llama dbo.zClasifProveedores
    #Haz un código de broma de hackeo donde pregunta si quiero hackear facebook y si contesto que si se ejecute metodo hackeofb
    #Es solo de broma no es algo verdadero y no son funciones verdaderas, es algo como
    #if (Quieres hackear fb? = si):
    #hackeo()
    #En lugar de print que sea un metodo o función como hackeo()
     
    return render(request, 'index.html')


