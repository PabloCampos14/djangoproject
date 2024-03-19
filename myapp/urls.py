#myapp/urls.py
from django.urls import path
from . import views 

urlpatterns = [
    path('', views.get_proveedores_list, name='get_proveedores_list'),
    #path('addProv/', views.addProv, name='add_prov'),
    path('updateprov/<int:id_proveedor>', views.updateprov, name= 'update_prov'),
    #path('deleteprov/<int:id_proveedor>', views.deleteprov, name= 'delete_prov'),
    path('search/<str:search_query>/', views.get_proveedores_list, name='search_proveedores_list'),
]