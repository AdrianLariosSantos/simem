from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from usuarios.models import Usuarios


@admin.register(Usuarios)
class UsuariosAdmin(UserAdmin):
    """Admin para el modelo personalizado de Usuarios"""
    list_display = ['username', 'email', 'nombre_completo', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active', 'is_superuser']
    search_fields = ['username', 'email', 'first_name', 'apellido_paterno', 'apellido_materno']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Información Adicional', {
            'fields': ('apellido_paterno', 'apellido_materno', 'numero_empleado')
        }),
    )
