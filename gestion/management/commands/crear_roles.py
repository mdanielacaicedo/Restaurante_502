"""
Comando para inicializar los roles del sistema
Uso: python manage.py crear_roles
"""
from django.core.management.base import BaseCommand
from gestion.models import Role


class Command(BaseCommand):
    help = 'Crea los roles predeterminados del sistema (administrador, mesero, cajero)'

    def handle(self, *args, **options):
        roles_data = [
            {
                'nombre': 'administrador',
                'descripcion': 'Acceso total al sistema, puede gestionar usuarios, roles, CRUD de todas entidades, facturas y reportes.'
            },
            {
                'nombre': 'mesero',
                'descripcion': 'Acceso a gestión de órdenes, mesas, menú y consulta de clientes.'
            },
            {
                'nombre': 'cajero',
                'descripcion': 'Acceso a facturación, pagos, órdenes y cierre de cuentas.'
            },
        ]

        creados = 0
        existentes = 0

        for rol_data in roles_data:
            rol, created = Role.objects.get_or_create(
                nombre=rol_data['nombre'],
                defaults={
                    'descripcion': rol_data['descripcion'],
                    'activo': True
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Rol "{rol.get_nombre_display()}" creado exitosamente')
                )
                creados += 1
            else:
                self.stdout.write(
                    self.style.WARNING(f'⚠ Rol "{rol.get_nombre_display()}" ya existía')
                )
                existentes += 1

        self.stdout.write(
            self.style.SUCCESS(f'\n✓ Proceso completado: {creados} roles creados, {existentes} ya existían.')
        )
