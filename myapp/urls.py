from django.urls import path
from . import views 

urlpatterns = [
    path('', views.get_proveedores_list),
    path('addProv/', views.addProv),
    path('updateprov/<int:id_proveedor>', views.updateprov),
    path('deleteprov/<int:id_proveedor>', views.deleteprov),

    
    path('prueba/', views.prueba),
    path('tabla/', views.get_proveedores_list),
    
    
]