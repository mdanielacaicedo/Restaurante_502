from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name = 'inicio'),
    path('clientes/', views.Lista_clientes, name = 'lista_clientes'),
    path('empleados/', views.Lista_empleados, name = 'lista_empleados'),
    path('mesas/', views.Lista_mesa, name = 'lista_mesas'),
    path('platos/', views.Lista_platos, name = 'lista_platos'),
    path('ordenes/', views.Lista_ordenes, name = 'lista_ordenes'),
    path('facturas/', views.Lista_facturas, name = 'lista_facturas'),
]