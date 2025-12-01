import django_filters
from catalogos.models import CatalogoHashTag


class CatalogoHashTagFilter(django_filters.FilterSet):
    """Filter para el modelo CatalogoHashTag"""
    id = django_filters.NumberFilter(field_name='id')
    descripcion = django_filters.CharFilter(field_name='descripcion', lookup_expr='icontains')
    activo = django_filters.BooleanFilter(field_name='activo')
    
    class Meta:
        model = CatalogoHashTag
        fields = ['descripcion', 'activo']
