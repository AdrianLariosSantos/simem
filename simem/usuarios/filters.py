import django_filters
from usuarios.models import Usuarios


class UsuariosFilter(django_filters.FilterSet):
    """Filter para el modelo Usuarios"""
    id = django_filters.NumberFilter(field_name='id')
    username = django_filters.CharFilter(field_name='username', lookup_expr='icontains')
    email = django_filters.CharFilter(field_name='email', lookup_expr='icontains')
    first_name = django_filters.CharFilter(field_name='first_name', lookup_expr='icontains')
    apellido_paterno = django_filters.CharFilter(field_name='apellido_paterno', lookup_expr='icontains')
    apellido_materno = django_filters.CharFilter(field_name='apellido_materno', lookup_expr='icontains')
    is_active = django_filters.BooleanFilter(field_name='is_active')
    is_staff = django_filters.BooleanFilter(field_name='is_staff')
    is_superuser = django_filters.BooleanFilter(field_name='is_superuser')
    
    class Meta:
        model = Usuarios
        fields = ['username', 'email', 'first_name', 'apellido_paterno', 'apellido_materno', 'is_active', 'is_staff']
