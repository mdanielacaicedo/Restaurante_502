# Generated migration for Role and UserRole models

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0002_factura_estado_factura_fecha_anulacion_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(choices=[('administrador', 'Administrador'), ('mesero', 'Mesero'), ('cajero', 'Cajero')], db_index=True, max_length=50, unique=True)),
                ('descripcion', models.TextField(blank=True)),
                ('activo', models.BooleanField(default=True)),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Rol',
                'verbose_name_plural': 'Roles',
                'db_table': 'Role',
            },
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asignado_en', models.DateTimeField(auto_now_add=True)),
                ('actualizado_en', models.DateTimeField(auto_now=True)),
                ('rol', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='usuarios', to='gestion.role')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='rol_info', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Rol de Usuario',
                'verbose_name_plural': 'Roles de Usuarios',
                'db_table': 'UserRole',
            },
        ),
    ]
