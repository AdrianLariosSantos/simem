from django.contrib import admin
from movilizaciones.models import Expedientes, Registro, HashTag_Registro


@admin.register(Expedientes)
class ExpedientesAdmin(admin.ModelAdmin):
    """Admin para el modelo Expedientes"""
    list_display = ['id', 'asunto', 'usuarios_id', 'fecha_evento', 'created_at']
    list_filter = ['fecha_evento', 'created_at']
    search_fields = ['asunto', 'descripcion', 'usuarios_id__username']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'fecha_evento'
    
    fieldsets = (
        ('Información General', {
            'fields': ('usuarios_id', 'asunto', 'fecha_evento')
        }),
        ('Detalles', {
            'fields': ('descripcion',)
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Registro)
class RegistroAdmin(admin.ModelAdmin):
    """Admin para el modelo Registro"""
    list_display = ['id', 'ubicacion', 'expedientes_id', 'creado_por', 'fecha', 'activo']
    list_filter = ['activo', 'fecha', 'created_at']
    search_fields = ['ubicacion', 'descripcion', 'creado_por__username']
    readonly_fields = ['fecha', 'hora', 'created_at', 'updated_at']
    date_hierarchy = 'fecha'
    
    fieldsets = (
        ('Información General', {
            'fields': ('expedientes_id', 'creado_por', 'ubicacion')
        }),
        ('Detalles', {
            'fields': ('descripcion', 'url_foto')
        }),
        ('Fecha y Hora', {
            'fields': ('fecha', 'hora')
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(HashTag_Registro)
class HashTagRegistroAdmin(admin.ModelAdmin):
    """Admin para el modelo HashTag_Registro"""
    list_display = ['id', 'id_catalogo_hashtag', 'id_registro', 'created_at']
    list_filter = ['created_at', 'id_catalogo_hashtag']
    search_fields = ['id_catalogo_hashtag__descripcion', 'id_registro__ubicacion']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
