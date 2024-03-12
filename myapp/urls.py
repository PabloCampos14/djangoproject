from django.urls import path
from . import views 

urlpatterns = [
    path('', views.get_proveedores_list, name='get_proveedores_list'),
    path('addProv/', views.addProv, name='add_prov'),
    path('updateprov/<int:id_proveedor>', views.updateprov, name= 'update_prov'),
    path('deleteprov/<int:id_proveedor>', views.deleteprov, name= 'delete_prov'),

    
    path('prueba/', views.prueba),
    path('tabla/', views.get_proveedores_list),
    
    
]