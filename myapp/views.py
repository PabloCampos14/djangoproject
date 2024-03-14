from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from .forms import ProvForm
from django.apps import apps
#from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import pyodbc
def prueba (request):
    
     
    return render(request, 'index.html')


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
    
    if search_query:
        cursor.execute("""
            SELECT p.id_proveedor, p.num_proveedor, p.nombre_proveedor, p.no_clabe, c.Descripcion
            FROM cxp_proveedor p
            LEFT JOIN zClasifProveedores c ON p.no_clabe = c.id_Clasif
            WHERE p.nombre_proveedor LIKE ? OR p.num_proveedor LIKE ? OR c.Descripcion LIKE ?
        """, ('%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%'))
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
    
    paginator = Paginator(proveedores_list, 11)  # 10 elementos por página

    page = request.GET.get('page')
    try:
        proveedores = paginator.page(page)
    except PageNotAnInteger:
        proveedores = paginator.page(1)
    except EmptyPage:
        proveedores = paginator.page(paginator.num_pages)

    return render(request, 'proveedores_list.html', {'search_query': search_query, 'proveedores': proveedores})




'''
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
    
    if search_query:
        cursor.execute("SELECT id_proveedor, num_proveedor, nombre_proveedor,no_clabe, Descripcion FROM cxp_proveedor WHERE nombre_proveedor LIKE ? OR num_proveedor LIKE ? OR Descripcion LIKE ?", ('%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%',))
        #cursor.execute("SELECT p.id_proveedor, p.num_proveedor, p.nombre_proveedor, p.no_clabe, c.Descripcion FROM cxp_proveedor p JOIN zClasifProveedores c ON p.no_clabe = c.id_Clasif WHERE p.nombre_proveedor LIKE ? OR p.num_proveedor LIKE ? OR c.Descripcion LIKE ?", ('%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%',))

    else:
        cursor.execute("SELECT id_proveedor, num_proveedor, nombre_proveedor,no_clabe, Descripcion FROM cxp_proveedor")

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
    
    paginator = Paginator(proveedores_list, 11)  # 10 elementos por página

    page = request.GET.get('page')
    try:
        proveedores = paginator.page(page)
    except PageNotAnInteger:
        proveedores = paginator.page(1)
    except EmptyPage:
        proveedores = paginator.page(paginator.num_pages)

    return render(request, 'proveedores_list.html', {'search_query': search_query, 'proveedores': proveedores})
'''
    #return render (request, 'proveedores_list.html', {'proveedores_list':proveedores_list}) #EL BUENO
#Ya ni se usa xd
def addProv(request):
    if request.method == 'GET':
        return render(request, 'addProv.html')
    if request.method == 'POST':
        form = ProvForm (request.POST)
        if form.is_valid():
            id_proveedor = form.cleaned_data.get("id_proveedor")
            num_proveedor = form.cleaned_data.get("num_proveedor")
            nombre_proveedor = form.cleaned_data.get("nombre_proveedor")
            razon_social = form.cleaned_data.get("razon_social")
            modulo_origen = form.cleaned_data.get("modulo_origen")
        conn = pyodbc.connect('Driver={sql server};'
                          'Server=gsvwdb17\sql2014;'
                          'Database=Pruebas3;'
                          'UID=gsvreportes;'
                          'PWD=Ind2019&;'
                          'Trusted_Connection=no;')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO dbo.cxp_proveedor(id_proveedor, num_proveedor, nombre_proveedor, razon_social, modulo_origen) VALUES (?, ?, ?, ?, ?)", 
                       id_proveedor, num_proveedor, nombre_proveedor, razon_social, modulo_origen)
        conn.commit()
        conn.close()


        return render(request, 'addProv.html', {'proveedores':{}})
    
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
def updateprov(request, id_proveedor):
    conn = pyodbc.connect('Driver={sql server};'
                          'Server=gsvwdb17\sql2014;'
                          'Database=Pruebas3;'
                          'UID=gsvreportes;'
                          'PWD=Ind2019&;'
                          'Trusted_Connection=no;')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dbo.cxp_proveedor WHERE id_proveedor = ?", id_proveedor)

    row = cursor.fetchone()
    if row:
        provider = {
            'id_proveedor': row[0],
            'nombre_proveedor': row[2],
            'no_clabe': row[3],
        }
    else:
        raise Http404("Proveedor not found")

    if request.method == 'POST':
        no_clabe = request.POST['no_clabe']
        description = {
            0: 'Refacciones',
            1: 'Largo plazo',
            2: 'Diesel',
            3: 'Llantas',
            4: 'InterCompañias',
            5: 'Administracion',
            6: 'Operacion',
            7: 'Permisioarios',
            8: 'Otros',
            9: 'CortoPlazo',
            10: 'LargoPlazoAnt',
            11: 'Diesel Ant',
            12: 'EPP',
            13: 'Infra',
            14: 'Limpieza',
            15: 'Seguridad',
            16: 'Uniformes',
        }.get(int(no_clabe), 'Unknown')
        cursor.execute("UPDATE dbo.cxp_proveedor SET no_clabe = ?, Descripcion = ? WHERE id_proveedor = ?", no_clabe, description, id_proveedor)
        conn.commit()
        
        return redirect('get_proveedores_list')
    else:
        
        return render(request, 'updateprov.html', {'provider': provider})
'''        
def deleteprov(request, id_proveedor ):
    conn = pyodbc.connect('Driver={sql server};'
                          'Server=gsvwdb17\sql2014;'
                          'Database=Pruebas3;'
                          'UID=gsvreportes;'
                          'PWD=Ind2019&;'
                          'Trusted_Connection=no;')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM dbo.cxp_proveedores where id_proveedor = ?", id_proveedor)
    conn.commit()
    conn.close()
    return redirect('get_proveedores_list')
    


