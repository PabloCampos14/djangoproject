from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from .forms import ProvForm
from django.http import Http404
from django.apps import apps
#from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.translation import activate
from .forms import EditarFechaForm
from django.utils import timezone
from datetime import datetime

import pyodbc


def connected():
    conn = pyodbc.connect('Driver={sql server};'
                          'Server=gsvwdb17\sql2014;'
                          'Database=Pruebas3;'
                          'UID=gsvreportes;'
                          'PWD=Ind2019&;'
                          'Trusted_Connection=no;')
    cursor = conn.cursor()
    cursor.execute("select * from zClasifProveedores")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

#@login_required(login_url='/accounts/acceder')
def get_proveedores_list(request):
    search_query = request.GET.get('search_query', None)
    proveedores_list = []
    
    # Tu cadena de conexión aquí
    conn = pyodbc.connect('Driver={sql server};'
                          'Server=gsvwdb17\sql2014;'
                          'Database=Pruebas3;'
                          'UID=gsvreportes;'
                          'PWD=Ind2019&;'
                          'Trusted_Connection=no;')
    
    cursor = conn.cursor()
    
    if search_query and search_query.lower() != "none":
        cursor.execute("""
            SELECT p.id_proveedor, p.num_proveedor, p.nombre_proveedor, p.no_clabe, c.Descripcion
            FROM cxp_proveedor p
            LEFT JOIN zClasifProveedores c ON p.no_clabe = c.id_Clasif
            WHERE p.nombre_proveedor LIKE ? OR p.num_proveedor LIKE ? OR c.Descripcion LIKE ? OR p.no_clabe LIKE ?
        """, ('%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%'))
    elif search_query and search_query.lower() == "none":
        cursor.execute("""
            SELECT p.id_proveedor, p.num_proveedor, p.nombre_proveedor, p.no_clabe, c.Descripcion
            FROM cxp_proveedor p
            LEFT JOIN zClasifProveedores c ON p.no_clabe = c.id_Clasif
            WHERE p.no_clabe IS NULL OR p.no_clabe = ''
        """)
    else:
        cursor.execute("""
            SELECT p.id_proveedor, p.num_proveedor, p.nombre_proveedor, p.no_clabe, c.Descripcion
            FROM cxp_proveedor p
            LEFT JOIN zClasifProveedores c ON p.no_clabe = c.id_Clasif
        """)

    for row in cursor.fetchall():
        proveedores_list.append({
            "id_proveedor": row[0],
            "num_proveedor": row[1],
            "nombre_proveedor": row[2],
            "no_clabe": row[3],
            "Descripcion": row[4]
        })
    cursor.close()
    conn.close()
    
    paginator = Paginator(proveedores_list, 21)  # 21 elementos mostrados por paginaaaaaa

    page = request.GET.get('page')
    try:
        proveedores = paginator.page(page)
    except PageNotAnInteger:
        proveedores = paginator.page(1)
    except EmptyPage:
        proveedores = paginator.page(paginator.num_pages)

    return render(request, 'proveedores_list.html', {'search_query': search_query, 'proveedores': proveedores})

    #return render (request, 'proveedores_list.html', {'proveedores_list':proveedores_list}) #EL BUENO
#Ya ni se usa xd

   
def updateprov(request, id_proveedor):
    conn = pyodbc.connect('Driver={sql server};'
                          'Server=gsvwdb17\sql2014;'
                          'Database=Pruebas3;'
                          'UID=gsvreportes;'
                          'PWD=Ind2019&;'
                          'Trusted_Connection=no;')
    cursor = conn.cursor()
    
    # Obtener los datos del proveedor
    cursor.execute("SELECT id_proveedor, nombre_proveedor, no_clabe FROM dbo.cxp_proveedor WHERE id_proveedor = ?", id_proveedor)
    row = cursor.fetchone()
    
    if row:
        provider = {
            'id_proveedor': row[0],
            'nombre_proveedor': row[1],
            'no_clabe': row[2],
        }
    else:
        raise Http404("Proveedor not found")
    
    # Obtener la descripción del proveedor desde la tabla zClasifProveedores
    cursor.execute("SELECT Descripcion FROM zClasifProveedores WHERE id_Clasif = ?", provider['no_clabe'])
    row = cursor.fetchone()
    if row:
        descripcion = row[0]
    else:
        descripcion = 'Unknown'  # En caso de que no se encuentre una descripción
    
    if request.method == 'POST':
        # Actualizar la columna no_clabe con los datos del formulario
        no_clabe = request.POST['no_clabe']
        cursor.execute("UPDATE dbo.cxp_proveedor SET no_clabe = ? WHERE id_proveedor = ?", no_clabe, id_proveedor)
        conn.commit()
        
        return redirect('get_proveedores_list')
    else:
        return render(request, 'updateprov.html', {'provider': provider, 'descripcion': descripcion})
    
'''
def login_view(request):
    if request.method == 'POST':
        id_usuario = request.POST.get('id_usuario')
        password = request.POST.get('password')

        # Realiza la conexión a la base de datos
        conn = pyodbc.connect('Driver={SQL Server};'
                              'Server=gsvwdb17\sql2014;'
                              'Database=Pruebas3;'
                              'UID=gsvreportes;'
                              'PWD=Ind2019&;'
                              'Trusted_Connection=no;')
        
        cursor = conn.cursor()

        # Realiza la consulta para validar las credenciales del usuario
        cursor.execute("SELECT * FROM dbo.seguridad_usuarios WHERE id_usuario = ? AND password = ?", (id_usuario, password))
        user = cursor.fetchone()

        if user:
            # Autenticación exitosa, redirige al usuario a la página deseada
            return redirect('get_proveedores_list')
        else:
            # Autenticación fallida
            return render(request, 'login.html', {'error_message': 'Invalid credentials'})
    else:
        # Renderiza el formulario de inicio de sesión
        return render(request, 'login.html')
'''

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
import pyodbc
from django.utils.translation import activate

import pyodbc
from django.shortcuts import render
from django.utils.translation import activate

def traficoLiquidacionMod(request, no_liquidacion=None, id_area=None):
    try:
        conn = pyodbc.connect('Driver={sql server};'
                              'Server=gsvwdb17\sql2014;'
                              'Database=Pruebas3;'
                              'UID=gsvreportes;'
                              'PWD=Ind2019&;'
                              'Trusted_Connection=no;')
        cursor = conn.cursor()
        activate('es')

        # Obtener los parámetros de búsqueda desde la URL
        no_liquidacion = request.GET.get('no_liquidacion', no_liquidacion)
        id_area = request.GET.get('id_area', id_area)

        # Consulta SQL base sin la condición de año específico
        consulta = """
            SELECT id_area, no_liquidacion, fecha_liquidacion, fecha_ingreso, fecha_ingreso2, no_poliza, id_cheque 
            FROM dbo.trafico_liquidacion
        """

        # Lista para almacenar resultados
        liquidaciones = []

        # Verificar si se proporcionaron parámetros de búsqueda válidos
        if no_liquidacion or id_area:
            # Construir la condición de búsqueda dinámica
            condiciones = []
            if no_liquidacion:
                condiciones.append(f"no_liquidacion = '{no_liquidacion}'")
            if id_area:
                condiciones.append(f"id_area = '{id_area}'")

            # Combinar condiciones en la consulta final si existen
            if condiciones:
                consulta += " WHERE " + " AND ".join(condiciones)

            # Ejecutar la consulta SQL modificada
            cursor.execute(consulta)

            # Obtener todas las filas de resultados
            for row in cursor.fetchall():
                # Crear un diccionario para cada fila y sus atributos
                liquidaciones.append({
                    "id_area": row[0],
                    "no_liquidacion": row[1],
                    "fecha_liquidacion": row[2],
                    "fecha_ingreso": row[3],    
                    "fecha_ingreso2": row[4],
                    "no_poliza": row[5],
                    "id_cheque": row[6]
                })

        # Cerrar cursor y conexión
        cursor.close()
        conn.close()

        # Renderizar la plantilla con los datos obtenidos y los parámetros de búsqueda
        return render(request, 'fechasMod.html', {'liquidaciones': liquidaciones, 'no_liquidacion': no_liquidacion, 'id_area': id_area})

    except Exception as e:
        # Manejo de excepciones: registrar el error y devolver una respuesta apropiada
        print(f"Error en la consulta: {e}")
        return render(request, 'fechasMod.html', {'error_message': 'Ocurrió un error al procesar la consulta.'})





from django.utils import timezone
from datetime import datetime

from django.utils import timezone

def editarFechaLiquidacion(request, no_liquidacion):
    conn = pyodbc.connect('Driver={sql server};'
                          'Server=gsvwdb17\sql2014;'
                          'Database=Pruebas3;'
                          'UID=gsvreportes;'
                          'PWD=Ind2019&;'
                          'Trusted_Connection=no;')
    cursor = conn.cursor()
    
    # Obtener la fecha de liquidación
    cursor.execute("SELECT fecha_liquidacion FROM dbo.trafico_liquidacion WHERE no_liquidacion = ?", no_liquidacion)
    row = cursor.fetchone()
    
    if row:
        fecha_liquidacion = row[0]
    else:
        raise Http404("Liquidación not found")
    
    if request.method == 'POST':
        # Actualizar la fecha de liquidación con los datos del formulario
        nueva_fecha_liquidacion_str = request.POST['fecha_liquidacion']
        nueva_fecha_liquidacion = datetime.strptime(nueva_fecha_liquidacion_str, '%Y-%m-%d').date()
        
        # Obtener la fecha actual
        fecha_actual = datetime.now().date()

# Validar que la nueva fecha pertenezca al mes y año actual
        if nueva_fecha_liquidacion.year != fecha_actual.year or nueva_fecha_liquidacion.month != fecha_actual.month:
            mensaje_error = "La fecha debe ser del mes y año actual."
            return render(request, 'editar_fecha_liquidacion.html', {'fecha_liquidacion': fecha_liquidacion, 'mensaje_error': mensaje_error})

# Formatear la nueva fecha como cadena para la consulta SQL
        nueva_fecha_liquidacion_str = nueva_fecha_liquidacion.strftime('%Y-%m-%d %H:%M:%S')

        
        # Ejecutar la consulta de actualización con la fecha formateada como cadena
        cursor.execute("UPDATE dbo.trafico_liquidacion SET fecha_liquidacion = ? WHERE no_liquidacion = ?", (nueva_fecha_liquidacion_str, no_liquidacion))
        conn.commit()
        
        return redirect('trafico_liquidacion')  # Redirigir a la lista de liquidaciones de tráfico
    else:
        return render(request, 'editar_fecha_liquidacion.html', {'form': EditarFechaForm()})








