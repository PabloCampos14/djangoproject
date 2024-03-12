from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
#from django.http import HttpResponse
#from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
#from django.urls import reverse
#from django.contrib import messages
#from django.contrib.messages.views import SuccessMessageMixin
#from .models import clasf_Proveedor_Tabla
from .forms import ProvForm
from django.apps import apps
from django.core.paginator import Paginator
import pyodbc
# ss
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
    proveedores_list = []
    
    # Tu cadena de conexión aquí
    conn = pyodbc.connect('Driver={sql server};'
                          'Server=gsvwdb17\sql2014;'
                          'Database=Pruebas3;'
                          'UID=gsvreportes;'
                          'PWD=Ind2019&;'
                          'Trusted_Connection=no;')
    
    cursor = conn.cursor()
    cursor.execute("SELECT id_proveedor, num_proveedor, nombre_proveedor,no_clabe FROM cxp_proveedor")
    #cursor.execute("Select p.no_clabe, p.id_proveedor, p.num_proveedor, p.nombre_proveedor, c.* from cxp_proveedor p left join zClasifProv c on p.no_clabe = c.id_clasif_prov ")


    for row in cursor.fetchall():
        proveedores_list.append({
            "id_proveedor": row[0], #
            "num_proveedor": row[1], #
            "nombre_proveedor": row[2],#
            "no_clabe": row[3]#,  Campo clabe unico editable
            
        })
    #paginator = Paginator(proveedores_list, 3)
    #pagina = request.Get.get("page") or 1
    #posts = paginator.get_page(pagina)
    #pagina_actual = int(pagina)
    #paginas = range(1, posts.paginator.num_pages + 1)
    cursor.close()
    conn.close()
    return render (request, 'proveedores_list.html', {'proveedores_list':proveedores_list})

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
    cursor.execute("SELECT * FROM dbo.cxp_proveedor WHERE id_proveedor = ?", id_proveedor)
    row = cursor.fetchone()
    if row:
        provider = {
            
            'no_clabe': row[3]
            
            # add other fields here
        }
    else:
        raise Http404("Proveedor not found")

    if request.method == 'POST':
        no_clabe = request.POST['no_clabe']
        cursor.execute("UPDATE dbo.cxp_proveedor SET no_clabe = ? WHERE id_proveedor = ?", no_clabe, id_proveedor)
        conn.commit()
        return redirect('get_proveedores_list')
    else:
        return render(request, 'updateprov.html', {'provider': provider})
    '''
    En la plantilla donde se muestra la tabla todo bien. y al dar al botón de "Edit" me manda a la plantilla para poder hacer la actualización de campo, ingreso en nuevo valor y al darle "submit" no pasa nada, no se guarda el nuevo valor
    if request.method == 'POST':
        form = ProvForm(request)
        if form.is_valid():
            num_proveedor = str(form.cleaned_data.get("num_proveedor"))
            nombre_proveedor = str(form.cleaned_data.get("nombre_proveedor"))
            razon_social = str(form.cleaned_data.get("razon_social"))
            modulo_origen = str(form.cleaned_data.get("modulo_origen"))
            cursor.execute("UPDATE dbo.cxp_proveedor SET num_proveedor = ?, nombre_proveedor = ?, razon_social= ?, modulo_origen = ?", 
                           num_proveedor, nombre_proveedor, razon_social, modulo_origen)
            conn.commit()
        conn.close()
        return redirect('get_proveedores_list')
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
    


