from django.http import Http404
from django.shortcuts import render, redirect
from .forms import ProvForm, EditarFechaForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.utils.translation import activate
from datetime import datetime
import pyodbc
from django.contrib.auth import authenticate, login
def connected():
    """
    Función para establecer una conexión con la base de datos y ejecutar una consulta de ejemplo.

    Returns:
        list: Resultado de la consulta.
    """
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



def get_proveedores_list(request):
    """
    Vista para mostrar una lista paginada de proveedores con búsqueda opcional.

    Args:
        request (HttpRequest): Objeto de solicitud HTTP.

    Returns:
        HttpResponse: Respuesta renderizada con la lista de proveedores.
    """
    search_query = request.GET.get('search_query', None)
    proveedores_list = []
    
    # Establecer conexión a la base de datos
    conn = pyodbc.connect('Driver={sql server};'
                          'Server=gsvwdb17\sql2014;'
                          'Database=Pruebas3;'
                          'UID=gsvreportes;'
                          'PWD=Ind2019&;'
                          'Trusted_Connection=no;')
    cursor = conn.cursor()
    
    # Construir y ejecutar la consulta SQL basada en la búsqueda opcional
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

    # Procesar los resultados de la consulta y agregar a la lista de proveedores
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
    
    # Paginar la lista de proveedores y renderizar la plantilla con los resultados
    paginator = Paginator(proveedores_list, 21)  # 21 elementos por página
    page = request.GET.get('page')
    try:
        proveedores = paginator.page(page)
    except PageNotAnInteger:
        proveedores = paginator.page(1)
    except EmptyPage:
        proveedores = paginator.page(paginator.num_pages)

    return render(request, 'proveedores_list.html', {'search_query': search_query, 'proveedores': proveedores})


def updateprov(request, id_proveedor):
    """
    Vista para actualizar los detalles de un proveedor.

    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        id_proveedor (int): ID del proveedor a actualizar.

    Returns:
        HttpResponse: Redirige a la lista de proveedores después de la actualización.
    """
    conn = pyodbc.connect('Driver={sql server};'
                          'Server=gsvwdb17\sql2014;'
                          'Database=Pruebas3;'
                          'UID=gsvreportes;'
                          'PWD=Ind2019&;'
                          'Trusted_Connection=no;')
    cursor = conn.cursor()
    
    # Obtener detalles del proveedor
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
        # Actualizar el número de clabe del proveedor
        no_clabe = request.POST['no_clabe']
        cursor.execute("UPDATE dbo.cxp_proveedor SET no_clabe = ? WHERE id_proveedor = ?", no_clabe, id_proveedor)
        conn.commit()
        
        return redirect('get_proveedores_list')
    else:
        return render(request, 'updateprov.html', {'provider': provider, 'descripcion': descripcion})


def traficoLiquidacionMod(request, no_liquidacion=None, id_area=None):
    """
    Vista para mostrar y filtrar las liquidaciones de tráfico.

    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        no_liquidacion (str, optional): Número de liquidación para filtrar. Defaults to None.
        id_area (str, optional): ID del área para filtrar. Defaults to None.

    Returns:
        HttpResponse: Renderiza la plantilla con las liquidaciones filtradas.
    """
    try:
        conn = pyodbc.connect('Driver={sql server};'
                              'Server=gsvwdb17\sql2014;'
                              'Database=Pruebas3;'
                              'UID=gsvreportes;'
                              'PWD=Ind2019&;'
                              'Trusted_Connection=no;')
        cursor = conn.cursor()
        activate('es')

        # Obtener parámetros de búsqueda desde la URL
        no_liquidacion = request.GET.get('no_liquidacion', no_liquidacion)
        id_area = request.GET.get('id_area', id_area)

        # Consulta base para las liquidaciones
        consulta = """
            SELECT id_area, no_liquidacion, fecha_liquidacion, fecha_ingreso, fecha_ingreso2, no_poliza, id_cheque 
            FROM dbo.trafico_liquidacion
        """

        # Lista para almacenar resultados
        liquidaciones = []

        # Construir y ejecutar consulta SQL con filtros opcionales
        if no_liquidacion or id_area:
            condiciones = []
            if no_liquidacion:
                condiciones.append(f"no_liquidacion = '{no_liquidacion}'")
            if id_area:
                condiciones.append(f"id_area = '{id_area}'")

            if condiciones:
                consulta += " WHERE " + " AND ".join(condiciones)

            cursor.execute(consulta)

            # Procesar los resultados y agregar a la lista de liquidaciones
            for row in cursor.fetchall():
                liquidaciones.append({
                    "id_area": row[0],
                    "no_liquidacion": row[1],
                    "fecha_liquidacion": row[2],
                    "fecha_ingreso": row[3],    
                    "fecha_ingreso2": row[4],
                    "no_poliza": row[5],
                    "id_cheque": row[6]
                })

        cursor.close()
        conn.close()

        return render(request, 'fechasMod.html', {'liquidaciones': liquidaciones, 'no_liquidacion': no_liquidacion, 'id_area': id_area})

    except Exception as e:
        print(f"Error en la consulta: {e}")
        return render(request, 'fechasMod.html', {'error_message': 'Ocurrió un error al procesar la consulta.'})


def editarFechaLiquidacion(request, no_liquidacion, id_area):
    try:
        conn = pyodbc.connect('Driver={SQL Server};'
                               'Server=gsvwdb17\sql2014;'
                               'Database=Pruebas3;'
                               'UID=gsvreportes;'
                               'PWD=Ind2019&;'
                               'Trusted_Connection=no;')
        cursor = conn.cursor()

        cursor.execute("""
            SELECT fecha_liquidacion, id_cheque, MONTH(fecha_liquidacion) AS mes, YEAR(fecha_liquidacion) AS año
            FROM dbo.trafico_liquidacion
            WHERE no_liquidacion = ? AND id_area = ?
        """, (no_liquidacion, id_area))
        row = cursor.fetchone()

        if not row:
            raise Http404("Liquidación no encontrada")

        fecha_liquidacion = row[0]
        id_cheque = row[1]
        mes_actual_registro = row[2]
        año_actual_registro = row[3]

        if request.method == 'POST':
            nueva_fecha_liquidacion_str = request.POST['fecha_liquidacion']
            nueva_fecha_liquidacion = datetime.strptime(nueva_fecha_liquidacion_str, '%Y-%m-%d').date()

            # Validar la fecha (mes y año) primero
            if nueva_fecha_liquidacion.month != mes_actual_registro or nueva_fecha_liquidacion.year != año_actual_registro:
                mensaje_error = f"La fecha debe ser del mismo mes y año que la fecha de liquidación actual ({mes_actual_registro} {año_actual_registro})."
                return render(request, 'editar_fecha_liquidacion.html', {'fecha_liquidacion': fecha_liquidacion, 'mensaje_error': mensaje_error})

            # Luego validar que id_cheque sea None
            if id_cheque is not None:
                mensaje_error = "No se puede modificar la fecha si el ID del cheque no es NULL."
                return render(request, 'editar_fecha_liquidacion.html', {'fecha_liquidacion': fecha_liquidacion, 'mensaje_error': mensaje_error})

            # Si pasa ambas validaciones, proceder con la actualización
            nueva_fecha_liquidacion_str = nueva_fecha_liquidacion.strftime('%Y-%m-%d')

            cursor.execute("""
                UPDATE dbo.trafico_liquidacion 
                SET fecha_liquidacion = ? 
                WHERE no_liquidacion = ? AND id_cheque IS NULL
            """, (nueva_fecha_liquidacion_str, no_liquidacion))
            conn.commit()

            return redirect('trafico_liquidacion')

        else:
            return render(request, 'editar_fecha_liquidacion.html', {'form': EditarFechaForm(), 'fecha_liquidacion': fecha_liquidacion})

    except Exception as e:
        print(f"Error en la consulta: {e}")
        return render(request, 'editar_fecha_liquidacion.html', {'error_message': 'Ocurrió un error al procesar la consulta.'})


