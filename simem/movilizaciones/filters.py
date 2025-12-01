import django_filters
from movilizaciones.models import Expedientes, Registro, HashTag_Registro


class ExpedientesFilter(django_filters.FilterSet):
    """Filter para el modelo Expedientes"""
    id = django_filters.NumberFilter(field_name='id')
    asunto = django_filters.CharFilter(field_name='asunto', lookup_expr='icontains')
    descripcion = django_filters.CharFilter(field_name='descripcion', lookup_expr='icontains')
    usuarios_id = django_filters.NumberFilter(field_name='usuarios_id')
    fecha_evento = django_filters.DateFromToRangeFilter(field_name='fecha_evento')
    
    class Meta:
        model = Expedientes
        fields = ['asunto', 'descripcion', 'usuarios_id', 'fecha_evento']


class RegistroFilter(django_filters.FilterSet):
    """Filter para el modelo Registro"""
    id = django_filters.NumberFilter(field_name='id')
    ubicacion = django_filters.CharFilter(field_name='ubicacion', lookup_expr='icontains')
    descripcion = django_filters.CharFilter(field_name='descripcion', lookup_expr='icontains')
    expedientes_id = django_filters.NumberFilter(field_name='expedientes_id')
    creado_por = django_filters.NumberFilter(field_name='creado_por')
    activo = django_filters.BooleanFilter(field_name='activo')
    fecha = django_filters.DateFromToRangeFilter(field_name='fecha')
    
    class Meta:
        model = Registro
        fields = ['ubicacion', 'descripcion', 'expedientes_id', 'creado_por', 'activo', 'fecha']


class HashTagRegistroFilter(django_filters.FilterSet):
    """Filter para el modelo HashTag_Registro"""
    id = django_filters.NumberFilter(field_name='id')
    id_catalogo_hashtag = django_filters.NumberFilter(field_name='id_catalogo_hashtag')
    id_registro = django_filters.NumberFilter(field_name='id_registro')
    
    class Meta:
        model = HashTag_Registro
        fields = ['id_catalogo_hashtag', 'id_registro']
