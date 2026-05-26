from django.contrib import admin
from .models import Cliente, Empleado, Mesa, Plato, Orden, DetalleOrden, Factura, Role, UserRole


class RoleAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion_corta', 'activo', 'creado_en')
    list_filter = ('activo',)
    readonly_fields = ('creado_en',)
    
    def descripcion_corta(self, obj):
        return obj.descripcion[:50] + '...' if len(obj.descripcion) > 50 else obj.descripcion
    descripcion_corta.short_description = 'Descripción'


class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'rol', 'asignado_en', 'actualizado_en')
    list_filter = ('rol', 'asignado_en')
    search_fields = ('usuario__username', 'usuario__email')
    readonly_fields = ('asignado_en', 'actualizado_en')
    
    fieldsets = (
        ('Información del Usuario', {
            'fields': ('usuario',)
        }),
        ('Rol Asignado', {
            'fields': ('rol',)
        }),
        ('Fechas', {
            'fields': ('asignado_en', 'actualizado_en'),
            'classes': ('collapse',)
        }),
    )


admin.site.register(Cliente)    
admin.site.register(Empleado)    
admin.site.register(Mesa)    
admin.site.register(Plato)    
admin.site.register(Orden)    
admin.site.register(DetalleOrden)    
admin.site.register(Factura)
admin.site.register(Role, RoleAdmin)
admin.site.register(UserRole, UserRoleAdmin)



