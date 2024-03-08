from django.urls import path
from . import views 

urlpatterns = [
    path('', views.get_proveedores_list),
    path('prueba/', views.prueba),
    path('tabla/', views.get_proveedores_list)
]