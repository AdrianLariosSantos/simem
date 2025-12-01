from django.contrib import admin
from catalogos.models import CatalogoHashTag


@admin.register(CatalogoHashTag)
class CatalogoHashTagAdmin(admin.ModelAdmin):
    """Admin para el modelo CatalogoHashTag"""
    list_display = ['id', 'descripcion', 'activo', 'created_at', 'updated_at']
    list_filter = ['activo', 'created_at']
    search_fields = ['descripcion']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
