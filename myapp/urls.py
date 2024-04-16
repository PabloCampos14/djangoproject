#myapp/urls.py
from django.urls import path
from . import views 

urlpatterns = [
    #path('', views.login_view, name='login'),  # URL para la vista de inicio de sesión
    path('', views.get_proveedores_list, name='get_proveedores_list'),
    #path('addProv/', views.addProv, name='add_prov'),
    path('updateprov/<int:id_proveedor>', views.updateprov, name= 'update_prov'),
    #path('deleteprov/<int:id_proveedor>', views.deleteprov, name= 'delete_prov'),
    path('search/<str:search_query>/', views.get_proveedores_list, name='search_proveedores_list'),
    #NUEVAS
    path('trafico-liquidacion/', views.traficoLiquidacionMod, name='trafico_liquidacion'),  # Nueva URL para la vista traficoLiquidacionMod
    #path('editar_fecha_liquidacion/<int:id_liquidacion>/', views.editarFechaLiquidacion, name='editar_fecha_liquidacion'),
    path('editar_fecha_liquidacion/<int:no_liquidacion>/<str:id_area>/', views.editarFechaLiquidacion, name='editar_fecha_liquidacion'),
    path('trafico-liquidacion/<str:no_liquidacion>/<str:id_area>/', views.traficoLiquidacionMod, name='trafico_liquidacion_search'),
    #path('eliminar-liquidacion/', views.eliminar_liquidacion, name='eliminar_liquidacion'),


]