from django.urls import path
from . import views 

urlpatterns = [
    path('', views.get_proveedores_list, name='get_proveedores_list'),
    path('addProv/', views.addProv, name='add_prov'),
    path('updateprov/<int:id_proveedor>', views.updateprov, name= 'update_prov'),
    path('deleteprov/<int:id_proveedor>', views.deleteprov, name= 'delete_prov'),

    
    path('prueba/', views.prueba),
    path('tabla/', views.get_proveedores_list),
    #Las url prueba/ y tabla/ nose usan para nada, son solo direcciones de prueba, la url donde se muestra mi tabla y donde se hace la busqueda es en path('', views.get_proveedores_list, name
    path('search/<str:search_query>/', views.get_proveedores_list, name='search_proveedores_list'),
]