from django.shortcuts import render
from django.http import HttpResponse 

# Create your views here.
def hello (request):

    return HttpResponse("<h2>Holaaaaaa</h2>")

def prueba (request):
    return HttpResponse("Prueba")
