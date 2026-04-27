from django.shortcuts import render

# Create your views here.
from .models import Cliente, Empleado, Mesa, Plato, Orden, Factura
def inicio(request):
    context = {
        'total_clientes': Cliente.objects.count(),
        'total_empleados': Empleado.objects.count(),
        'total_mesas': Mesa.objects.count(),
        'total_platos': Plato.objects.count(),
        'total_ordenes': Orden.objects.count(),
        'total_facturas': Factura.objects.count(),
    }
    return render(request, 'gestion/inicio.html', context)

def Lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'gestion/clientes.html', {'clientes': clientes})

def Lista_empleados(request):
    empleados = Empleado.objects.all()
    return render(request, 'gestion/empleados.html', {'empleados': empleados})

def Lista_mesa(request):
    mesas = Mesa.objects.all()
    return render(request, 'gestion/mesas.html', {'mesas': mesas})

def Lista_platos(request):
    platos = Plato.objects.all()
    return render(request, 'gestion/platos.html', {'platos': platos})

def Lista_ordenes(request):
    ordenes = Orden.objects.all()
    return render(request, 'gestion/ordenes.html', {'ordenes': ordenes})

def Lista_facturas(request):
    facturas = Factura.objects.all()
    return render(request, 'gestion/facturas.html', {'facturas': facturas})


