from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
#from django.urls import reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from .models import clasf_Proveedor_Tabla
import pyodbc
'''
class ClasifListado(ListView):
    model = clasf_Proveedor_Tabla

class ClasifCrear(SuccessMessageMixin, CreateView):
    model = clasf_Proveedor_Tabla
    fields = "__all__"
    success_message = "Clasificación creada correctamente"

    def get_success_url(self):
        return reverse('leer')

class ClasifDetalle(DetailView):
    model = clasf_Proveedor_Tabla

class ClasifActualizar(SuccessMessageMixin, UpdateView):
    model = clasf_Proveedor_Tabla
    fields = "__all__"
    success_message = "Registro actualizado correctamente"

    def get_success_url(self):
        return reverse('leer')

class ClasifEliminar(SuccessMessageMixin, DeleteView):
    model = clasf_Proveedor_Tabla

    def get_success_url(self):
        success_message = 'Clasificación eliminada correctamente'
        messages.success(self.request, success_message)
        return reverse('leer')

# Vista para la conexión a la base de datos
def hello(request):
    try:
        with pyodbc.connect('Driver={sql server};'
                            'Server=gsvwdb17\sql2014;'
                            'Database=Pruebas3;'
                            'UID=gsvreportes;'
                            'PWD=Ind2019&;'
                            'Trusted_Connection=no;') as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM zClasifProveedores"
            cursor.execute(query)
            result = cursor.fetchall()
            # Puedes hacer algo con el resultado aquí, como pasarlo al contexto y renderizar en una plantilla
            return render(request, 'index.html', {'result': result})
    except pyodbc.Error as e:
        # Manejar el error según tus necesidades
        return HttpResponse(f"Error de base de datos: {e}")

    #return render(request, 'misplantillas.html', {'clasf_Proveedor_Tabla': result})
'''


'''

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
        '''

'''
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

'''
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
            "portal_multiple": row[34]
        })
    cursor.close()
    conn.close()
    return render (request, 'proveedores_list.html', {'proveedores_list':proveedores_list})


