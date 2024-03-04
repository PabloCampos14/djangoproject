from django.shortcuts import render
from django.http import HttpResponse 
from django.template import Template, Context
from .forms import ReclasificadorForm
import pyodbc

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

def pizarron(request):
    #configuración de la base de datos
    server = "gsvwdb17\sql2014"
    db = "Pruebas3"
    user = "gsvreportes"
    password = "Ind2019&"

    #Se intenta realizar la conexión con la base de datos
    
    try:
        #Construcción de la cadena de conexión
        connection_string = "DRIVER = {SQL Server};SERVER ="+server+";DATABASE="+db+";UID="+ user+ ";PWD="+password
        #edoConexion= True
        conn = pyodbc.connect(connection_string)

        #creación de cursor
        cursor = conn.cursor()

        #Consulta a la tabla de la base de datos
        #sql_query = "SELECT * FROM dbo.zClasifProveedores"
        sql_query = "SELECT * FROM dbo.zClasifProveedores"

        #Ejecución de consulta
        cursor.execute(sql_query)

        # Obtener nombres de campos
        #nombres_campos = [column[0] for column in cursor.description]
        nombres_campos = [column[0] for column in cursor.description]


        # Obtener valores de la consulta
        #valores = cursor.fetchall()
        valores = cursor.fetchall()

        cursor.close()
        conn.close()
        #return render(request, "misplantillas.html", {"edoconect": True, "clasificaciones": valores, "nombreCampo": nombres_campos})

        return render(request, "tablaplantilla.html", {"edoconect": True, "clasificaciones": valores, "nombreCampo": nombres_campos})

    except Exception as e:

        return render(request, "tablaplantilla.html", {"edoconect": False, "error_message": str(e)})

def prueba (request):
    #Temporalmente vacío en lo que se me ocurre que poner en esta extensión xd
    #Me equivoqué la tabla de la base de datos se llama dbo.zClasifProveedores
    return render(request, 'index.html')

