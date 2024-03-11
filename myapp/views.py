from django.http import Http404
from django.shortcuts import render, redirect
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
    cursor.execute("SELECT * FROM cxp_proveedor")
    #cursor.execute("Select p.no_clabe, p.id_proveedor, p.num_proveedor, p.nombre_proveedor, c.* from cxp_proveedor p left join zClasifProv c on p.no_clabe = c.id_clasif_prov ")


    for row in cursor.fetchall():
        proveedores_list.append({
            "id_proveedor": row[0],
            "num_proveedor": row[1],
            "nombre_proveedor": row[2],
            "razon_social": row[3],
            "modulo_origen": row[4],
            "idprov_ref": row[5],
            "status_prov": row[6],
            "fecha_status": row[7],
            "id_ingreso": row[8],
            "fecha_ingreso": row[9],
            "observaciones": row[10],
            "descto_prontopago": row[11],
            "diascredito": row[12],
            "id_concepto": row[13],
            "cuenta": row[14],
            "subcuenta": row[15],
            "auxiliar1": row[16],
            "direccion": row[17],
            "rfc": row[18],
            "tipo_beneficiario": row[19],
            "no_clabe": row[20],
            "tipo": row[21],
            "id_compania": row[22],
            "tipo_proveedor": row[23],
            "view_diot": row[24],
            "calficacion": row[25],
            "proveedor_logo": row[26],
            "id_ProvBco": row[27],
            "revisado": row[28],
            "id_area": row[29],
            "aplica_eval": row[30],
            "critico": row[31],
            "contacto": row[32],
            "prod_serv": row[33],
            "portal_multiple": row[34]#,
            #"id_clasif": row[35],
            #"descripcion_clasif": row[36]
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
    pv = []
    conn = pyodbc.connect('Driver={sql server};'
                          'Server=gsvwdb17\sql2014;'
                          'Database=Pruebas3;'
                          'UID=gsvreportes;'
                          'PWD=Ind2019&;'
                          'Trusted_Connection=no;')
    cursor = conn.cursor()
    if request.method == 'GET':
        cursor.execute("SELECT * FROM dbo.cxp_proveedor WHERE id_proveedor = ?", id_proveedor)
        for row in cursor.fetchall():
            pv.append({"id_proveedor": row[0], "num_proveedor": row[1], "nombre_proveedor": row[2], "razon_social": row[3], "modulo_origen": row[4]})
        conn.close()
        return render (request, "addProv.html", {'proveedor':pv[0]})
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
    


