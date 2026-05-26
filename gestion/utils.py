from functools import wraps
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import UserRole, Role


def obtener_rol_usuario(usuario):
 
    if not usuario.is_authenticated:
        return None
    
    try:
        user_role = UserRole.objects.select_related('rol').get(usuario=usuario)
        return user_role.rol.nombre
    except UserRole.DoesNotExist:
        return None


def obtener_nombre_rol(rol):
  
    ROLES_NOMBRES = {
        'administrador': 'Administrador',
        'mesero': 'Mesero',
        'cajero': 'Cajero',
    }
    return ROLES_NOMBRES.get(rol, rol)


def usuario_tiene_rol(usuario, roles_requeridos):
   
    if isinstance(roles_requeridos, str):
        roles_requeridos = [roles_requeridos]
    
    rol_usuario = obtener_rol_usuario(usuario)
    return rol_usuario in roles_requeridos


def requerir_rol(*roles_permitidos):
   
    def decorador(vista):
        @wraps(vista)
        def wrapper(request, *args, **kwargs):
       
            if not request.user.is_authenticated:
                return render(
                    request,
                    'gestion/acceso_requerido_login.html',
                    {},
                    status=401
                )
            
            rol_usuario = obtener_rol_usuario(request.user)
            if not rol_usuario:
                messages.error(request, 'Tu usuario no tiene un rol asignado. Contacta al administrador.')
                return redirect('inicio')
            
            
            if rol_usuario not in roles_permitidos:
                messages.error(
                    request,
                    f'No tienes permiso para acceder a esta función. Se requiere ser {", ".join([obtener_nombre_rol(r) for r in roles_permitidos])}.'
                )
                
                return render(
                    request,
                    'gestion/403.html',
                    {'rol': rol_usuario},
                    status=403
                )
            
            return vista(request, *args, **kwargs)
        return wrapper
    return decorador


def requerir_rol_ajax(*roles_permitidos):

    def decorador(vista):
        @wraps(vista)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseForbidden(
                    '{"error": "No autenticado"}',
                    content_type='application/json'
                )
            
            rol_usuario = obtener_rol_usuario(request.user)
            if rol_usuario not in roles_permitidos:
                return HttpResponseForbidden(
                    '{"error": "Acceso denegado - rol insuficiente"}',
                    content_type='application/json'
                )
            
            return vista(request, *args, **kwargs)
        return wrapper
    return decorador

PERMISOS_POR_ROL = {
    'administrador': {
        'puede_ver_clientes': True,
        'puede_crear_cliente': True,
        'puede_editar_cliente': True,
        'puede_eliminar_cliente': True,
        
        'puede_ver_empleados': True,
        'puede_crear_empleado': True,
        'puede_editar_empleado': True,
        'puede_eliminar_empleado': True,
        
        'puede_ver_mesas': True,
        'puede_crear_mesa': True,
        'puede_editar_mesa': True,
        'puede_eliminar_mesa': True,
        
        'puede_ver_platos': True,
        'puede_crear_plato': True,
        'puede_editar_plato': True,
        'puede_eliminar_plato': True,
        
        'puede_ver_ordenes': True,
        'puede_crear_orden': True,
        'puede_editar_orden': True,
        'puede_eliminar_orden': True,
        'puede_facturar_orden': True,
        
        'puede_ver_facturas': True,
        'puede_crear_factura': True,
        'puede_anular_factura': True,
        
        'puede_ver_usuarios': True,
        'puede_crear_usuario': True,
        'puede_editar_usuario': True,
        'puede_eliminar_usuario': True,
        'puede_asignar_roles': True,
        
        'puede_ver_reportes': True,
    },
    
    'mesero': {
        'puede_ver_clientes': True,
        'puede_crear_cliente': False,
        'puede_editar_cliente': False,
        'puede_eliminar_cliente': False,
        
        'puede_ver_empleados': False,
        'puede_crear_empleado': False,
        'puede_editar_empleado': False,
        'puede_eliminar_empleado': False,
        
        'puede_ver_mesas': True,
        'puede_crear_mesa': False,
        'puede_editar_mesa': False,
        'puede_eliminar_mesa': False,
        
        'puede_ver_platos': True,
        'puede_crear_plato': False,
        'puede_editar_plato': False,
        'puede_eliminar_plato': False,
        
        'puede_ver_ordenes': True,
        'puede_crear_orden': True,
        'puede_editar_orden': True,
        'puede_eliminar_orden': False,
        'puede_facturar_orden': False,
        
        'puede_ver_facturas': False,
        'puede_crear_factura': False,
        'puede_anular_factura': False,
        
        'puede_ver_usuarios': False,
        'puede_crear_usuario': False,
        'puede_editar_usuario': False,
        'puede_eliminar_usuario': False,
        'puede_asignar_roles': False,
        
        'puede_ver_reportes': False,
    },
    
    'cajero': {
        'puede_ver_clientes': True,
        'puede_crear_cliente': False,
        'puede_editar_cliente': False,
        'puede_eliminar_cliente': False,
        
        'puede_ver_empleados': False,
        'puede_crear_empleado': False,
        'puede_editar_empleado': False,
        'puede_eliminar_empleado': False,
        
        'puede_ver_mesas': True,
        'puede_crear_mesa': False,
        'puede_editar_mesa': False,
        'puede_eliminar_mesa': False,
        
        'puede_ver_platos': False,
        'puede_crear_plato': False,
        'puede_editar_plato': False,
        'puede_eliminar_plato': False,
        
        'puede_ver_ordenes': True,
        'puede_crear_orden': False,
        'puede_editar_orden': False,
        'puede_eliminar_orden': False,
        'puede_facturar_orden': True,
        
        'puede_ver_facturas': True,
        'puede_crear_factura': True,
        'puede_anular_factura': True,
        
        'puede_ver_usuarios': False,
        'puede_crear_usuario': False,
        'puede_editar_usuario': False,
        'puede_eliminar_usuario': False,
        'puede_asignar_roles': False,
        
        'puede_ver_reportes': False,
    },
}


def obtener_permisos_usuario(usuario):
    
    rol = obtener_rol_usuario(usuario)
    if not rol:
      
        return {
            f'puede_{accion}': False
            for accion in ['ver_clientes', 'crear_cliente', 'editar_cliente', 'eliminar_cliente',
                          'ver_empleados', 'crear_empleado', 'editar_empleado', 'eliminar_empleado',
                          'ver_mesas', 'crear_mesa', 'editar_mesa', 'eliminar_mesa',
                          'ver_platos', 'crear_plato', 'editar_plato', 'eliminar_plato',
                          'ver_ordenes', 'crear_orden', 'editar_orden', 'eliminar_orden', 'facturar_orden',
                          'ver_facturas', 'crear_factura', 'anular_factura',
                          'ver_usuarios', 'crear_usuario', 'editar_usuario', 'eliminar_usuario', 'asignar_roles',
                          'ver_reportes']
        }
    
    return PERMISOS_POR_ROL.get(rol, {})


def usuario_puede(usuario, permiso):
  
    permisos = obtener_permisos_usuario(usuario)
    return permisos.get(permiso, False)


def agregar_rol_contexto(request, context=None):
  
    if context is None:
        context = {}
    
    context['rol'] = obtener_rol_usuario(request.user)
    context['permisos'] = obtener_permisos_usuario(request.user)
    
    return context
