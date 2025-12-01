from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

from usuarios.models import Usuarios
from usuarios.serializers import (
    UsuariosSerializer,
    UsuariosListSerializer,
    UsuariosRetrieveSerializer,
    UsuariosCreateSerializer,
    UsuariosUpdateSerializer,
)
from usuarios.filters import UsuariosFilter
from helpers.exceptions import BadRequest, NotFound, Unauthorized
from helpers.responses import (
    ok_response,
    created_response,
    bad_request_response,
    not_found_response,
    no_content_response,
)
from helpers.errors import error


class UsuariosViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar usuarios.
    Permite CRUD completo sobre usuarios del sistema con control de permisos.
    """
    queryset = Usuarios.objects.all()
    serializer_class = UsuariosSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = UsuariosFilter
    search_fields = ['username', 'email', 'first_name', 'apellido_paterno', 'apellido_materno']
    ordering_fields = ['date_joined', 'username']
    ordering = ['-date_joined']

    def get_serializer_class(self):
        """Retorna el serializador según la acción"""
        serializers_map = {
            'list': UsuariosListSerializer,
            'retrieve': UsuariosRetrieveSerializer,
            'create': UsuariosCreateSerializer,
            'update': UsuariosUpdateSerializer,
            'partial_update': UsuariosUpdateSerializer,
        }
        return serializers_map.get(self.action, self.serializer_class)

    def get_permissions(self):
        """Permite crear usuarios sin autenticación, pero requiere autenticación para otras acciones"""
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        """Filtra usuarios según permisos del usuario actual"""
        if self.request.user.is_superuser:
            return Usuarios.objects.all().order_by('-date_joined')
        return Usuarios.objects.filter(is_active=True).order_by('-date_joined')

    def get_object(self):
        """Obtiene un objeto con manejo de excepciones"""
        try:
            obj_id = self.kwargs.get('pk')
            obj = self.get_queryset().get(pk=obj_id)
            self.check_object_permissions(self.request, obj)
            return obj
        except ObjectDoesNotExist:
            return None

    def list(self, request, *args, **kwargs):
        """Lista usuarios con paginación"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return ok_response(data=self.get_paginated_response(serializer.data).data)
        serializer = self.get_serializer(queryset, many=True)
        return ok_response(data=serializer.data)

    def retrieve(self, request, pk=None):
        """Obtiene un usuario específico"""
        instance = self.get_object()
        if not instance:
            raise NotFound()
        serializer = self.get_serializer(instance)
        return ok_response(data=serializer.data)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """Crear un nuevo usuario"""
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            new_error = error(default_errors=serializer.errors)
            raise BadRequest(new_error)
        serializer.save()
        return created_response(data=serializer.data)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        """Actualizar usuario completo"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if not instance:
            raise NotFound()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid():
            new_error = error(default_errors=serializer.errors)
            raise BadRequest(new_error)
        serializer.save()
        return ok_response(data=serializer.data)

    def partial_update(self, request, *args, **kwargs):
        """Actualización parcial de usuario"""
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        """Desactivar usuario (eliminación lógica)"""
        instance = self.get_object()
        if not instance:
            raise NotFound()
        instance.is_active = False
        instance.save()
        return ok_response(data=None, message='Usuario desactivado correctamente')

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        """Obtiene el usuario actual"""
        serializer = UsuariosRetrieveSerializer(request.user)
        return ok_response(data=serializer.data)

    @action(detail=False, methods=['get'])
    def activos(self, request):
        """Obtiene solo usuarios activos"""
        usuarios_activos = Usuarios.objects.filter(is_active=True).order_by('username')
        serializer = UsuariosListSerializer(usuarios_activos, many=True)
        return ok_response(data=serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def cambiar_contraseña(self, request, pk=None):
        """Cambiar contraseña de un usuario"""
        usuario = self.get_object()
        if not usuario:
            raise NotFound()

        password_antigua = request.data.get('password_antigua')
        password_nueva = request.data.get('password_nueva')
        confirm_password = request.data.get('confirm_password')

        if not password_antigua or not password_nueva or not confirm_password:
            raise BadRequest({'error': 'Todos los campos de contraseña son requeridos'})

        if not usuario.check_password(password_antigua):
            raise BadRequest({'error': 'La contraseña anterior es incorrecta'})

        if password_nueva != confirm_password:
            raise BadRequest({'error': 'Las contraseñas nuevas no coinciden'})

        usuario.set_password(password_nueva)
        usuario.save()

        return ok_response(data=None, message='Contraseña actualizada correctamente')
