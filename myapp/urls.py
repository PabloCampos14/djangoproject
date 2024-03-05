from django.urls import path
from . import views 

urlpatterns = [
    path('', views.hello),
    path('prueba/', views.prueba),
    path('tabla/', views.tabla)
]