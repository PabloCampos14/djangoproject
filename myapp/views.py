from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from .forms import ProvForm
from django.apps import apps
#from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
    
    paginator = Paginator(proveedores_list, 21)  # 21 elementos por página - Como se empieza desde cero xd

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



