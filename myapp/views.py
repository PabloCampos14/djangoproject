from django.shortcuts import render
from django.http import HttpResponse 
from django.template import Template, Context

# Create your views here.
def hello (request):
    doc_externo = open("C:/Users/SistemasGSV/Desktop/djangoproject/myapp/Plantillas/misplantillas.html")
    plt = Template(doc_externo.read()) #Se deben importar Template y context

    doc_externo.close

    cxt = Context()

    documento = plt.render(cxt)

    return HttpResponse(documento)

def prueba (request):
    doc_externo_prueba = open("C:/Users/SistemasGSV/Desktop/djangoproject/myapp/Plantillas/index.html")
    plt_prueba = Template(doc_externo_prueba.read()) #Se deben importar Template y context

    doc_externo_prueba.close

    cxt_prueba = Context()

    documento_prueba = plt_prueba.render(cxt_prueba)

    return HttpResponse(documento_prueba)

