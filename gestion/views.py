from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cliente, Empleado, Mesa, Plato, Orden, DetalleOrden, Factura, Role, UserRole
from .utils import requerir_rol, obtener_rol_usuario, usuario_puede, obtener_permisos_usuario, agregar_rol_contexto
from decimal import Decimal

# Vistas Para Autenticación

def login_view(request):
    """Vista para iniciar sesión"""
    if request.user.is_authenticated:
        return redirect('inicio')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenido {user.username}')
            return redirect('inicio')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'gestion/login.html')


def register_view(request):
    """Vista para registrarse"""
    if request.user.is_authenticated:
        return redirect('inicio')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Validaciones
        if not username or not email or not password1:
            messages.error(request, 'Por favor completa todos los campos')
        elif password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'El usuario ya existe')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'El correo ya está registrado')
        else:
            # Crear usuario
            user = User.objects.create_user(username=username, email=email, password=password1)
            login(request, user)
            messages.success(request, 'Registro exitoso. Bienvenido al sistema')
            return redirect('inicio')
    
    return render(request, 'gestion/register.html')


def logout_view(request):
    """Vista para cerrar sesión"""
    logout(request)
    messages.success(request, 'Sesión cerrada exitosamente')
    return redirect('login')



# Vistas para el dashboard y CRUD de cada modelo

@login_required
def inicio(request):
    """Panel principal del dashboard"""
    rol = obtener_rol_usuario(request.user)
    permisos = obtener_permisos_usuario(request.user)
    
    context = {
        'total_clientes': Cliente.objects.count(),
        'total_empleados': Empleado.objects.count(),
        'total_mesas': Mesa.objects.count(),
        'total_platos': Plato.objects.count(),
        'total_ordenes': Orden.objects.count(),
        'total_facturas': Factura.objects.count(),
        'rol': rol,
        'permisos': permisos,
    }
    return render(request, 'gestion/inicio.html', context)


# CRUD para cada modelo: Cliente, Empleado, Mesa, Plato, Orden, Factura
# CRUD Cliente

@requerir_rol('administrador', 'mesero', 'cajero')
def Lista_clientes(request):
    """Listar todos los clientes"""
    clientes = Cliente.objects.all().order_by('-id')
    context = agregar_rol_contexto(request, {'clientes': clientes})
    return render(request, 'gestion/clientes.html', context)


@requerir_rol('administrador')
def crear_cliente(request):
    """Crear nuevo cliente"""
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        telefono = request.POST.get('telefono')
        correo = request.POST.get('correo')
        
        if not nombre:
            messages.error(request, 'El nombre es requerido')
        else:
            Cliente.objects.create(
                nombre=nombre,
                telefono=telefono,
                correo=correo
            )
            messages.success(request, 'Cliente creado exitosamente')
            return redirect('lista_clientes')
    
    return render(request, 'gestion/cliente_form.html')


@requerir_rol('administrador')
def editar_cliente(request, id):
    """Editar cliente"""
    cliente = get_object_or_404(Cliente, id=id)
    
    if request.method == 'POST':
        cliente.nombre = request.POST.get('nombre', cliente.nombre)
        cliente.telefono = request.POST.get('telefono', cliente.telefono)
        cliente.correo = request.POST.get('correo', cliente.correo)
        
        if not cliente.nombre:
            messages.error(request, 'El nombre es requerido')
        else:
            cliente.save()
            messages.success(request, 'Cliente actualizado exitosamente')
            return redirect('lista_clientes')
    
    return render(request, 'gestion/cliente_form.html', {'cliente': cliente})


@requerir_rol('administrador')
def eliminar_cliente(request, id):
    """Eliminar cliente"""
    cliente = get_object_or_404(Cliente, id=id)
    
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente eliminado exitosamente')
        return redirect('lista_clientes')
    
    return render(request, 'gestion/cliente_confirm_delete.html', {'cliente': cliente})



# CRUD Empleado


@requerir_rol('administrador')
def Lista_empleados(request):
    """Listar todos los empleados"""
    empleados = Empleado.objects.all().order_by('-id')
    context = agregar_rol_contexto(request, {'empleados': empleados})
    return render(request, 'gestion/empleados.html', context)


@requerir_rol('administrador')
def crear_empleado(request):
    """Crear nuevo empleado"""
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        cargo = request.POST.get('cargo')
        telefono = request.POST.get('telefono')
        correo = request.POST.get('correo')
        
        if not nombre or not cargo:
            messages.error(request, 'El nombre y cargo son requeridos')
        else:
            Empleado.objects.create(
                nombre=nombre,
                cargo=cargo,
                telefono=telefono,
                correo=correo
            )
            messages.success(request, 'Empleado creado exitosamente')
            return redirect('lista_empleados')
    
    cargos = Empleado.CARGOS
    return render(request, 'gestion/empleado_form.html', {'cargos': cargos})


@requerir_rol('administrador')
def editar_empleado(request, id):
    """Editar empleado"""
    empleado = get_object_or_404(Empleado, id=id)
    
    if request.method == 'POST':
        empleado.nombre = request.POST.get('nombre', empleado.nombre)
        empleado.cargo = request.POST.get('cargo', empleado.cargo)
        empleado.telefono = request.POST.get('telefono', empleado.telefono)
        empleado.correo = request.POST.get('correo', empleado.correo)
        
        if not empleado.nombre or not empleado.cargo:
            messages.error(request, 'El nombre y cargo son requeridos')
        else:
            empleado.save()
            messages.success(request, 'Empleado actualizado exitosamente')
            return redirect('lista_empleados')
    
    cargos = Empleado.CARGOS
    return render(request, 'gestion/empleado_form.html', {'empleado': empleado, 'cargos': cargos})


@requerir_rol('administrador')
def eliminar_empleado(request, id):
    """Eliminar empleado"""
    empleado = get_object_or_404(Empleado, id=id)
    
    if request.method == 'POST':
        empleado.delete()
        messages.success(request, 'Empleado eliminado exitosamente')
        return redirect('lista_empleados')
    
    return render(request, 'gestion/empleado_confirm_delete.html', {'empleado': empleado})



# CRUD Mesa


@requerir_rol('administrador', 'mesero', 'cajero')
def Lista_mesa(request):
    """Listar todas las mesas"""
    mesas = Mesa.objects.all().order_by('numero_mesa')
    context = agregar_rol_contexto(request, {'mesas': mesas})
    return render(request, 'gestion/mesas.html', context)


@requerir_rol('administrador')
def crear_mesa(request):
    """Crear nueva mesa"""
    if request.method == 'POST':
        numero_mesa = request.POST.get('numero_mesa')
        capacidad = request.POST.get('capacidad')
        
        if not numero_mesa or not capacidad:
            messages.error(request, 'El número de mesa y capacidad son requeridos')
        elif Mesa.objects.filter(numero_mesa=numero_mesa).exists():
            messages.error(request, 'Ya existe una mesa con este número')
        else:
            Mesa.objects.create(
                numero_mesa=int(numero_mesa),
                capacidad=int(capacidad)
            )
            messages.success(request, 'Mesa creada exitosamente')
            return redirect('lista_mesas')
    
    return render(request, 'gestion/mesa_form.html')


@requerir_rol('administrador')
def editar_mesa(request, id):
    """Editar mesa"""
    mesa = get_object_or_404(Mesa, id=id)
    
    if request.method == 'POST':
        numero_mesa = request.POST.get('numero_mesa', mesa.numero_mesa)
        capacidad = request.POST.get('capacidad', mesa.capacidad)
        estado = request.POST.get('estado_mesa', mesa.estado_mesa)
        
        # Validar que no exista otra mesa con el mismo número
        if str(numero_mesa) != str(mesa.numero_mesa) and Mesa.objects.filter(numero_mesa=numero_mesa).exists():
            messages.error(request, 'Ya existe una mesa con este número')
        else:
            mesa.numero_mesa = int(numero_mesa)
            mesa.capacidad = int(capacidad)
            mesa.estado_mesa = estado
            mesa.save()
            messages.success(request, 'Mesa actualizada exitosamente')
            return redirect('lista_mesas')
    
    estados = Mesa.ESTADOS_MESA
    return render(request, 'gestion/mesa_form.html', {'mesa': mesa, 'estados': estados})


@requerir_rol('administrador')
def eliminar_mesa(request, id):
    """Eliminar mesa"""
    mesa = get_object_or_404(Mesa, id=id)
    
    if request.method == 'POST':
        mesa.delete()
        messages.success(request, 'Mesa eliminada exitosamente')
        return redirect('lista_mesas')
    
    return render(request, 'gestion/mesa_confirm_delete.html', {'mesa': mesa})


# CRUD Plato

@requerir_rol('administrador', 'mesero', 'cajero')
def Lista_platos(request):
    """Listar todos los platos"""
    platos = Plato.objects.all().order_by('-id')
    context = agregar_rol_contexto(request, {'platos': platos})
    return render(request, 'gestion/platos.html', context)


@requerir_rol('administrador')
def crear_plato(request):
    """Crear nuevo plato"""
    if request.method == 'POST':
        nombre_plato = request.POST.get('nombre_plato')
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio')
        categoria = request.POST.get('categoria')
        disponible = request.POST.get('disponible') == 'on'
        
        if not nombre_plato or not precio:
            messages.error(request, 'El nombre y precio son requeridos')
        else:
            Plato.objects.create(
                nombre_plato=nombre_plato,
                descripcion=descripcion,
                precio=Decimal(precio),
                categoria=categoria,
                disponible=disponible
            )
            messages.success(request, 'Plato creado exitosamente')
            return redirect('lista_platos')
    
    return render(request, 'gestion/plato_form.html')


@requerir_rol('administrador')
def editar_plato(request, id):
    """Editar plato"""
    plato = get_object_or_404(Plato, id=id)
    
    if request.method == 'POST':
        plato.nombre_plato = request.POST.get('nombre_plato', plato.nombre_plato)
        plato.descripcion = request.POST.get('descripcion', plato.descripcion)
        plato.precio = Decimal(request.POST.get('precio', plato.precio))
        plato.categoria = request.POST.get('categoria', plato.categoria)
        plato.disponible = request.POST.get('disponible') == 'on'
        
        if not plato.nombre_plato or not plato.precio:
            messages.error(request, 'El nombre y precio son requeridos')
        else:
            plato.save()
            messages.success(request, 'Plato actualizado exitosamente')
            return redirect('lista_platos')
    
    return render(request, 'gestion/plato_form.html', {'plato': plato})


@requerir_rol('administrador')
def eliminar_plato(request, id):
    """Eliminar plato"""
    plato = get_object_or_404(Plato, id=id)
    
    if request.method == 'POST':
        plato.delete()
        messages.success(request, 'Plato eliminado exitosamente')
        return redirect('lista_platos')
    
    return render(request, 'gestion/plato_confirm_delete.html', {'plato': plato})



# CRUD Orden


@requerir_rol('administrador', 'mesero', 'cajero')
def Lista_ordenes(request):
    """Listar todas las órdenes"""
    ordenes = Orden.objects.all().order_by('-fecha_hora')
    context = agregar_rol_contexto(request, {'ordenes': ordenes})
    return render(request, 'gestion/ordenes.html', context)


@requerir_rol('administrador', 'mesero')
def crear_orden(request):
    """Crear nueva orden con platos"""
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')
        empleado_id = request.POST.get('empleado')
        mesa_id = request.POST.get('mesa')
        
        if not cliente_id or not empleado_id or not mesa_id:
            messages.error(request, 'Cliente, empleado y mesa son requeridos')
        else:
            cliente = get_object_or_404(Cliente, id=cliente_id)
            empleado = get_object_or_404(Empleado, id=empleado_id)
            mesa = get_object_or_404(Mesa, id=mesa_id)
            
            orden = Orden.objects.create(
                cliente=cliente,
                empleado=empleado,
                mesa=mesa
            )
            
            # Procesar platos
            platos_data = request.POST.getlist('platos')
            for key in request.POST:
                if key.startswith('platos[') and '][plato]' in key:
                    # Extraer el índice
                    index = key.split('[')[1].split(']')[0]
                    plato_id = request.POST.get(f'platos[{index}][plato]')
                    cantidad = request.POST.get(f'platos[{index}][cantidad]')
                    
                    if plato_id and cantidad:
                        try:
                            plato = get_object_or_404(Plato, id=plato_id)
                            DetalleOrden.objects.create(
                                orden=orden,
                                plato=plato,
                                cantidad=int(cantidad)
                            )
                        except Exception as e:
                            messages.warning(request, f'Error al agregar plato: {str(e)}')
            
            messages.success(request, 'Orden creada exitosamente')
            return redirect('editar_orden', id=orden.id)
    
    context = {
        'clientes': Cliente.objects.all(),
        'empleados': Empleado.objects.all(),
        'mesas': Mesa.objects.all(),
        'platos': Plato.objects.filter(disponible=True),
    }
    return render(request, 'gestion/orden_form.html', context)


@requerir_rol('administrador', 'mesero')
def editar_orden(request, id):
    """Editar orden y sus detalles"""
    orden = get_object_or_404(Orden, id=id)
    
    if request.method == 'POST':
        orden.estado_orden = request.POST.get('estado_orden', orden.estado_orden)
        orden.save()
        messages.success(request, 'Orden actualizada exitosamente')
    
    detalles = orden.detalles.all()
    platos = Plato.objects.filter(disponible=True)
    
    context = {
        'orden': orden,
        'detalles': detalles,
        'platos': platos,
        'estados': Orden.ESTADOS_ORDEN,
    }
    return render(request, 'gestion/orden_detail.html', context)


@requerir_rol('administrador', 'mesero')
def agregar_detalle_orden(request, orden_id):
    """Agregar detalle a una orden"""
    orden = get_object_or_404(Orden, id=orden_id)
    
    if request.method == 'POST':
        plato_id = request.POST.get('plato')
        cantidad = request.POST.get('cantidad')
        
        if not plato_id or not cantidad:
            messages.error(request, 'Plato y cantidad son requeridos')
        else:
            plato = get_object_or_404(Plato, id=plato_id)
            DetalleOrden.objects.create(
                orden=orden,
                plato=plato,
                cantidad=int(cantidad)
            )
            messages.success(request, 'Detalle agregado a la orden')
    
    return redirect('editar_orden', id=orden_id)


@requerir_rol('administrador', 'mesero')
def eliminar_detalle_orden(request, id):
    """Eliminar detalle de una orden"""
    detalle = get_object_or_404(DetalleOrden, id=id)
    orden_id = detalle.orden.id
    
    detalle.delete()
    
    # Recalcular el total de la orden
    total = sum((d.subtotal or Decimal('0.00')) for d in detalle.orden.detalles.all())
    detalle.orden.total = total
    detalle.orden.save()
    
    messages.success(request, 'Detalle eliminado de la orden')
    return redirect('editar_orden', id=orden_id)


@requerir_rol('administrador')
def eliminar_orden(request, id):
    """Eliminar orden"""
    orden = get_object_or_404(Orden, id=id)
    
    if request.method == 'POST':
        orden.delete()
        messages.success(request, 'Orden eliminada exitosamente')
        return redirect('lista_ordenes')
    
    return render(request, 'gestion/orden_confirm_delete.html', {'orden': orden})



# CRUD Factura


@requerir_rol('administrador', 'cajero')
def Lista_facturas(request):
    # Listar todas las facturas con filtro opcional
    ver_todas = request.GET.get('ver_todas', False)
    
    if ver_todas:
        facturas = Factura.objects.all().order_by('-fecha_factura')
        estado_filtro = 'todas'
    else:
        facturas = Factura.objects.filter(estado='activa').order_by('-fecha_factura')
        estado_filtro = 'activas'
    
    context = agregar_rol_contexto(request, {
        'facturas': facturas,
        'estado_filtro': estado_filtro,
        'total_activas': Factura.objects.filter(estado='activa').count(),
        'total_anuladas': Factura.objects.filter(estado='anulada').count(),
    })
    return render(request, 'gestion/facturas.html', context)


@requerir_rol('administrador', 'cajero')
def crear_factura(request):
    """Crear nueva factura"""
    ordenes_sin_factura = Orden.objects.exclude(factura__isnull=False)
    
    if request.method == 'POST':
        orden_id = request.POST.get('orden')
        metodo_pago = request.POST.get('metodo_pago')
        impuesto_porcentaje = Decimal('0.19')  # 19% de IVA (Colombia)
        
        if not orden_id:
            messages.error(request, 'Debe seleccionar una orden')
        else:
            orden = get_object_or_404(Orden, id=orden_id)
            
            if hasattr(orden, 'factura'):
                messages.error(request, 'Esta orden ya tiene factura')
            else:
                subtotal = orden.total
                impuesto = subtotal * impuesto_porcentaje
                total_factura = subtotal + impuesto
                
                Factura.objects.create(
                    orden=orden,
                    subtotal=subtotal,
                    impuesto=impuesto,
                    total_factura=total_factura,
                    metodo_pago=metodo_pago
                )
                orden.estado_orden = 'Facturada'
                orden.save()
                
                messages.success(request, 'Factura creada exitosamente')
                return redirect('lista_facturas')
    
    metodos_pago = Factura.METODOS_PAGO
    context = {
        'ordenes': ordenes_sin_factura,
        'metodos_pago': metodos_pago,
    }
    return render(request, 'gestion/factura_form.html', context)


@requerir_rol('administrador', 'cajero')
def eliminar_factura(request, id):
    """Anular factura """
    factura = get_object_or_404(Factura, id=id)
    
    if not factura.puede_ser_anulada():
        messages.error(request, 'Esta factura no puede ser anulada porque ya está anulada')
        return redirect('lista_facturas')
    
    if request.method == 'POST':
        razon_anulacion = request.POST.get('razon_anulacion', 'No especificada')
        factura.anular(razon=razon_anulacion)
        factura.orden.estado_orden = 'Entregada'
        factura.orden.save()
        messages.success(request, f'Factura #{factura.id} anulada exitosamente. Razón: {razon_anulacion}')
        return redirect('lista_facturas')
    
    return render(request, 'gestion/factura_confirm_delete.html', {'factura': factura})


@requerir_rol('administrador', 'cajero')
def facturar_orden(request, orden_id):

    orden = get_object_or_404(Orden, id=orden_id)
    
    if hasattr(orden, 'factura'):
        messages.error(request, 'Esta orden ya tiene factura')
        return redirect('editar_orden', id=orden_id)
    
    if not orden.detalles.exists():
        messages.error(request, 'La orden debe tener al menos un detalle')
        return redirect('editar_orden', id=orden_id)
    
    if request.method == 'POST':
        metodo_pago = request.POST.get('metodo_pago')
        impuesto_porcentaje = Decimal('0.19')  # 19% de IVA (Colombia)
        
        if not metodo_pago:
            messages.error(request, 'Debe seleccionar un método de pago')
        else:
            subtotal = orden.total
            impuesto = subtotal * impuesto_porcentaje
            total_factura = subtotal + impuesto
            
            factura = Factura.objects.create(
                orden=orden,
                subtotal=subtotal,
                impuesto=impuesto,
                total_factura=total_factura,
                metodo_pago=metodo_pago,
                estado='activa'
            )
            
            orden.estado_orden = 'Facturada'
            orden.save()
            
            messages.success(request, f'Factura #{factura.id} creada exitosamente')
            return redirect('editar_orden', id=orden_id)
    
    metodos_pago = Factura.METODOS_PAGO
    context = {
        'orden': orden,
        'metodos_pago': metodos_pago,
    }
    return render(request, 'gestion/facturar_orden.html', context)


