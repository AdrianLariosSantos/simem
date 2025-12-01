from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from catalogos.models import CatalogoHashTag
from catalogos.serializers import (
    CatalogoHashTagSerializer,
    CatalogoHashTagListSerializer,
    CatalogoHashTagCreateSerializer,
    CatalogoHashTagUpdateSerializer,
)
from catalogos.filters import CatalogoHashTagFilter
from helpers.exceptions import BadRequest, NotFound
from helpers.responses import (
    ok_response,
    created_response,
    no_content_response,
)
from helpers.errors import error


class CatalogoHashTagViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar catálogos de hashtags.
    Permite CRUD completo sobre los hashtags disponibles.
    """
    queryset = CatalogoHashTag.objects.all()
    serializer_class = CatalogoHashTagSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CatalogoHashTagFilter
    search_fields = ['descripcion']
    ordering_fields = ['descripcion', 'created_at']
    ordering = ['descripcion']

    def get_serializer_class(self):
        """Retorna el serializador según la acción"""
        serializers_map = {
            'list': CatalogoHashTagListSerializer,
            'retrieve': CatalogoHashTagListSerializer,
            'create': CatalogoHashTagCreateSerializer,
            'update': CatalogoHashTagUpdateSerializer,
            'partial_update': CatalogoHashTagUpdateSerializer,
        }
        return serializers_map.get(self.action, self.serializer_class)

    def get_queryset(self):
        """Filtra hashtags según el estado activo"""
        queryset = CatalogoHashTag.objects.all()
        # Si no es superuser, solo ve hashtags activos
        if not self.request.user.is_superuser:
            queryset = queryset.filter(activo=True)
        return queryset

    def get_object(self):
        """Obtiene un objeto con manejo de excepciones"""
        try:
            obj_id = self.kwargs.get('pk')
            obj = self.get_queryset().get(pk=obj_id)
            return obj
        except ObjectDoesNotExist:
            return None

    def list(self, request, *args, **kwargs):
        """Lista hashtags con paginación"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return ok_response(data=self.get_paginated_response(serializer.data).data)
        serializer = self.get_serializer(queryset, many=True)
        return ok_response(data=serializer.data)

    def retrieve(self, request, pk=None):
        """Obtiene un hashtag específico"""
        instance = self.get_object()
        if not instance:
            raise NotFound()
        serializer = self.get_serializer(instance)
        return ok_response(data=serializer.data)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """Crear un nuevo hashtag"""
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            new_error = error(default_errors=serializer.errors)
            raise BadRequest(new_error)
        serializer.save()
        return created_response(data=serializer.data)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        """Actualizar hashtag completo"""
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
        """Actualización parcial de hashtag"""
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        """Eliminar lógico del hashtag (marcar como inactivo)"""
        instance = self.get_object()
        if not instance:
            raise NotFound()
        instance.activo = False
        instance.save()
        return ok_response(data=None, message='Hashtag desactivado correctamente')

    @action(detail=False, methods=['get'])
    def activos(self, request):
        """Obtiene solo hashtags activos"""
        hashtags_activos = CatalogoHashTag.objects.filter(activo=True).order_by('descripcion')
        serializer = CatalogoHashTagListSerializer(hashtags_activos, many=True)
        return ok_response(data=serializer.data)
