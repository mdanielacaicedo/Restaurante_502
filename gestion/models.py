from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from .validators import validar_solo_numeros, validar_nombre, validar_numero_mesa, validar_capacidad_mesa, validar_precio, validar_cantidad


class Cliente(models.Model):
    nombre = models.CharField(max_length=100, validators=[validar_nombre])
    telefono = models.CharField(max_length=20, blank=True, null=True, validators=[validar_solo_numeros])
    correo = models.EmailField(unique=True, blank=True, null=True)

    class Meta:
        db_table = 'Cliente'

    def __str__(self):
        return self.nombre


class Empleado(models.Model):
    CARGOS = [
        ('Mesero', 'Mesero'),
        ('Mesera', 'Mesera'),
        ('Cajero', 'Cajero'),
        ('Cajera', 'Cajera'),
        ('Administrador', 'Administrador'),
    ]

    nombre = models.CharField(max_length=100, validators=[validar_nombre])
    cargo = models.CharField(max_length=50, choices=CARGOS)
    telefono = models.CharField(max_length=20, blank=True, null=True, validators=[validar_solo_numeros])
    correo = models.EmailField(unique=True, blank=True, null=True)

    class Meta:
        db_table = 'Empleado'

    def __str__(self):
        return f"{self.nombre} - {self.cargo}"


class Mesa(models.Model):
    ESTADOS_MESA = [
        ('Disponible', 'Disponible'),
        ('Ocupada', 'Ocupada'),
        ('Reservada', 'Reservada'),
    ]

    numero_mesa = models.PositiveIntegerField(unique=True, validators=[validar_numero_mesa])
    capacidad = models.PositiveIntegerField(validators=[validar_capacidad_mesa])
    estado_mesa = models.CharField(max_length=20, choices=ESTADOS_MESA, default='Disponible')

    class Meta:
        db_table = 'Mesa'

    def __str__(self):
        return f"Mesa {self.numero_mesa}"


class Plato(models.Model):
    nombre_plato = models.CharField(max_length=100, validators=[validar_nombre])
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, validators=[validar_precio])
    categoria = models.CharField(max_length=50, blank=True, null=True)
    disponible = models.BooleanField(default=True)

    class Meta:
        db_table = 'Plato'

    def __str__(self):
        return self.nombre_plato


class Orden(models.Model):
    ESTADOS_ORDEN = [
        ('Activa', 'Activa'),
        ('En preparación', 'En preparación'),
        ('Entregada', 'Entregada'),
        ('Facturada', 'Facturada'),
        ('Cancelada', 'Cancelada'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    estado_orden = models.CharField(max_length=20, choices=ESTADOS_ORDEN, default='Activa')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        db_table = 'OrdenRestaurante'

    def __str__(self):
        return f"Orden {self.id} - {self.cliente.nombre}"


class DetalleOrden(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name='detalles')
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(validators=[validar_cantidad])
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'Detalle_Orden'

    def save(self, *args, **kwargs):
        self.precio_unitario = self.plato.precio
        self.subtotal = Decimal(self.cantidad) * self.precio_unitario
        super().save(*args, **kwargs)

        total_orden = sum((detalle.subtotal or Decimal('0.00')) for detalle in self.orden.detalles.all())
        self.orden.total = total_orden
        self.orden.save()

    def __str__(self):
        return f"Detalle {self.id} - Orden {self.orden.id}"


class Factura(models.Model):
    METODOS_PAGO = [
        ('Efectivo', 'Efectivo'),
        ('Tarjeta', 'Tarjeta'),
        ('Transferencia', 'Transferencia'),
        ('Nequi', 'Nequi'),
        ('Daviplata', 'Daviplata'),
    ]

    ESTADOS_FACTURA = [
        ('activa', 'Activa'),
        ('anulada', 'Anulada'),
    ]

    orden = models.OneToOneField(Orden, on_delete=models.CASCADE)
    fecha_factura = models.DateTimeField(auto_now_add=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    impuesto = models.DecimalField(max_digits=10, decimal_places=2)
    total_factura = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=30, choices=METODOS_PAGO)
    estado = models.CharField(max_length=20, choices=ESTADOS_FACTURA, default='activa')
    fecha_anulacion = models.DateTimeField(blank=True, null=True)
    razon_anulacion = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'Factura'

    def __str__(self):
        return f"Factura {self.id} - Orden {self.orden.id} ({self.get_estado_display()})"

    def anular(self, razon=''):
        from django.utils import timezone
        self.estado = 'anulada'
        self.fecha_anulacion = timezone.now()
        self.razon_anulacion = razon
        self.save()

    def puede_ser_editada(self):       
        return self.estado == 'activa'

    def puede_ser_anulada(self):
        return self.estado == 'activa'


class Role(models.Model):
   
    NOMBRE_CHOICES = [
        ('administrador', 'Administrador'),
        ('mesero', 'Mesero'),
        ('cajero', 'Cajero'),
    ]

    nombre = models.CharField(
        max_length=50,
        choices=NOMBRE_CHOICES,
        unique=True,
        db_index=True
    )
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Role'
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.get_nombre_display()


class UserRole(models.Model):

    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='rol_info'
    )
    rol = models.ForeignKey(
        Role,
        on_delete=models.PROTECT,
        related_name='usuarios'
    )
    asignado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'UserRole'
        verbose_name = 'Rol de Usuario'
        verbose_name_plural = 'Roles de Usuarios'

    def __str__(self):
        return f"{self.usuario.username} - {self.rol.get_nombre_display()}"
