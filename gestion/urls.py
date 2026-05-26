from django.urls import path
from . import views

urlpatterns = [
    # Autenticación
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Inicio
    path('', views.inicio, name='inicio'),
    
    # Cliente URLs
    path('clientes/', views.Lista_clientes, name='lista_clientes'),
    path('clientes/crear/', views.crear_cliente, name='crear_cliente'),
    path('clientes/<int:id>/editar/', views.editar_cliente, name='editar_cliente'),
    path('clientes/<int:id>/eliminar/', views.eliminar_cliente, name='eliminar_cliente'),
    
    # Empleado URLs
    path('empleados/', views.Lista_empleados, name='lista_empleados'),
    path('empleados/crear/', views.crear_empleado, name='crear_empleado'),
    path('empleados/<int:id>/editar/', views.editar_empleado, name='editar_empleado'),
    path('empleados/<int:id>/eliminar/', views.eliminar_empleado, name='eliminar_empleado'),
    
    # Mesa URLs
    path('mesas/', views.Lista_mesa, name='lista_mesas'),
    path('mesas/crear/', views.crear_mesa, name='crear_mesa'),
    path('mesas/<int:id>/editar/', views.editar_mesa, name='editar_mesa'),
    path('mesas/<int:id>/eliminar/', views.eliminar_mesa, name='eliminar_mesa'),
    
    # Plato URLs
    path('platos/', views.Lista_platos, name='lista_platos'),
    path('platos/crear/', views.crear_plato, name='crear_plato'),
    path('platos/<int:id>/editar/', views.editar_plato, name='editar_plato'),
    path('platos/<int:id>/eliminar/', views.eliminar_plato, name='eliminar_plato'),
    
    # Orden URLs
    path('ordenes/', views.Lista_ordenes, name='lista_ordenes'),
    path('ordenes/crear/', views.crear_orden, name='crear_orden'),
    path('ordenes/<int:id>/editar/', views.editar_orden, name='editar_orden'),
    path('ordenes/<int:id>/eliminar/', views.eliminar_orden, name='eliminar_orden'),
    path('ordenes/<int:orden_id>/agregar-detalle/', views.agregar_detalle_orden, name='agregar_detalle_orden'),
    path('ordenes/detalle/<int:id>/eliminar/', views.eliminar_detalle_orden, name='eliminar_detalle_orden'),
    
    # Factura URLs
    path('facturas/', views.Lista_facturas, name='lista_facturas'),
    path('facturas/crear/', views.crear_factura, name='crear_factura'),
    path('facturas/<int:id>/eliminar/', views.eliminar_factura, name='eliminar_factura'),
]