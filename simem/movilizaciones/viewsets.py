from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

from movilizaciones.models import Expedientes, Registro, HashTag_Registro
from movilizaciones.serializers import (
    ExpedientesSerializer,
    ExpedientesListSerializer,
    ExpedientesDetailSerializer,
    ExpedientesCreateSerializer,
    RegistroSerializer,
    RegistroDetailSerializer,
    RegistroCreateSerializer,
    RegistroUpdateSerializer,
    HashTagRegistroSerializer
)
from movilizaciones.filters import ExpedientesFilter, RegistroFilter, HashTagRegistroFilter
from helpers.exceptions import BadRequest, NotFound
from helpers.responses import (
    ok_response,
    created_response,
    no_content_response,
)
from helpers.errors import error
from django.core.files.storage import default_storage
from django.utils.text import get_valid_filename
from uuid import uuid4
import os


class ExpedientesViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar expedientes.
    Permite CRUD completo sobre expedientes del sistema.
    """
    queryset = Expedientes.objects.all()
    serializer_class = ExpedientesSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ExpedientesFilter
    search_fields = ['asunto', 'descripcion']
    ordering_fields = ['fecha_evento', 'created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """Retorna el serializador según la acción"""
        serializers_map = {
            'list': ExpedientesListSerializer,
            'retrieve': ExpedientesDetailSerializer,
            'create': ExpedientesCreateSerializer,
        }
        return serializers_map.get(self.action, self.serializer_class)

    def get_queryset(self):
        """Filtra expedientes según permisos"""
        if self.request.user.is_superuser:
            return Expedientes.objects.all().order_by('-created_at')
        return Expedientes.objects.filter(usuarios_id=self.request.user).order_by('-created_at')

    def get_object(self):
        """Obtiene un objeto con manejo de excepciones"""
        try:
            obj_id = self.kwargs.get('pk')
            obj = self.get_queryset().get(pk=obj_id)
            return obj
        except ObjectDoesNotExist:
            return None

    def list(self, request, *args, **kwargs):
        """Lista expedientes con paginación"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return ok_response(data=self.get_paginated_response(serializer.data).data)
        serializer = self.get_serializer(queryset, many=True)
        return ok_response(data=serializer.data)

    def retrieve(self, request, pk=None):
        """Obtiene un expediente específico"""
        instance = self.get_object()
        if not instance:
            raise NotFound()
        serializer = self.get_serializer(instance)
        return ok_response(data=serializer.data)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """Crear un nuevo expediente"""
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            new_error = error(default_errors=serializer.errors)
            raise BadRequest(new_error)
        serializer.save(usuarios_id=request.user)
        return created_response(data=serializer.data)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        """Actualizar expediente"""
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
        """Actualización parcial de expediente"""
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        """Eliminar expediente"""
        instance = self.get_object()
        if not instance:
            raise NotFound()
        instance.delete()
        return ok_response(data=None, message='Expediente eliminado correctamente')

    @action(detail=True, methods=['get'])
    def registros(self, request, pk=None):
        """Obtiene todos los registros asociados a un expediente"""
        expediente = self.get_object()
        if not expediente:
            raise NotFound()
        registros = expediente.registros.all().order_by('-created_at')
        serializer = RegistroSerializer(registros, many=True)
        return ok_response(data=serializer.data)


class RegistroViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar registros de movilizaciones.
    Permite CRUD completo sobre registros del sistema.
    """
    queryset = Registro.objects.all()
    serializer_class = RegistroSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = RegistroFilter
    search_fields = ['ubicacion', 'descripcion']
    ordering_fields = ['fecha', 'hora', 'created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """Retorna el serializador según la acción"""
        serializers_map = {
            'list': RegistroSerializer,
            'retrieve': RegistroDetailSerializer,
            'create': RegistroCreateSerializer,
            'update': RegistroUpdateSerializer,
            'partial_update': RegistroUpdateSerializer,
        }
        return serializers_map.get(self.action, self.serializer_class)

    def get_queryset(self):
        """Filtra registros según permisos"""
        if self.request.user.is_superuser:
            return Registro.objects.all().order_by('-created_at')
        return Registro.objects.filter(
            Q(creado_por=self.request.user) | Q(expedientes_id__usuarios_id=self.request.user)
        ).order_by('-created_at')

    def get_object(self):
        """Obtiene un objeto con manejo de excepciones"""
        try:
            obj_id = self.kwargs.get('pk')
            obj = self.get_queryset().get(pk=obj_id)
            return obj
        except ObjectDoesNotExist:
            return None

    def list(self, request, *args, **kwargs):
        """Lista registros con paginación"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return ok_response(data=self.get_paginated_response(serializer.data).data)
        serializer = self.get_serializer(queryset, many=True)
        return ok_response(data=serializer.data)

    def retrieve(self, request, pk=None):
        """Obtiene un registro específico"""
        instance = self.get_object()
        if not instance:
            raise NotFound()
        serializer = self.get_serializer(instance)
        return ok_response(data=serializer.data)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """Crear un nuevo registro"""
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            new_error = error(default_errors=serializer.errors)
            raise BadRequest(new_error)
        serializer.save(creado_por=request.user)
        return created_response(data=serializer.data)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        """Actualizar registro"""
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
        """Actualización parcial de registro"""
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        """Eliminar registro lógico"""
        instance = self.get_object()
        if not instance:
            raise NotFound()
        instance.activo = False
        instance.save()
        return ok_response(data=None, message='Registro desactivado correctamente')

    @action(detail=True, methods=['post'], url_path='upload-foto')
    @transaction.atomic
    def upload_foto(self, request, pk=None):
        """
        Sube una imagen para el registro y guarda el archivo en el servidor.
        Reglas:
        - Máximo 12MB
        - Sólo tipos de contenido de imagen
        - Carpeta: expedientes/<expediente_id>/registros/<registro_id>/
        Devuelve la URL absoluta en `url_foto`.
        """
        registro = self.get_object()
        if not registro:
            raise NotFound()

        file = request.FILES.get('file') or request.FILES.get('foto') or request.FILES.get('image')
        if not file:
            raise BadRequest({'file': 'Archivo de imagen requerido (clave: file|foto|image).'})

        # Validación de tamaño (12 MB)
        max_size = 12 * 1024 * 1024  # 12MB
        if file.size > max_size:
            raise BadRequest({'file': 'El archivo excede el límite de 12MB.'})

        # Validación de tipo simple
        content_type = getattr(file, 'content_type', '') or ''
        if not content_type.startswith('image/'):
            raise BadRequest({'file': 'Sólo se permiten archivos de imagen.'})

        # Construcción de ruta: expedientes/<expediente_id>/registros/<registro_id>/<uuid>.<ext>
        expediente_id = registro.expedientes_id_id
        base_dir = os.path.join('expedientes', str(expediente_id), 'registros', str(registro.id))
        original_name = get_valid_filename(getattr(file, 'name', 'upload'))
        _, ext = os.path.splitext(original_name)
        filename = f"{uuid4().hex}{ext.lower()}"
        relative_path = os.path.join(base_dir, filename)

        # Guardar usando el storage por defecto
        saved_path = default_storage.save(relative_path, file)
        file_url = default_storage.url(saved_path)

        # Guardar URL absoluta en el campo url_foto
        try:
            absolute_url = request.build_absolute_uri(file_url)
        except Exception:
            absolute_url = file_url

        registro.url_foto = absolute_url
        registro.save(update_fields=['url_foto', 'updated_at'])

        serializer = self.get_serializer(registro)
        return ok_response(data=serializer.data, message='Imagen cargada correctamente')

    @action(detail=True, methods=['post'])
    def agregar_hashtag(self, request, pk=None):
        """Agregar un hashtag a un registro.
        Si la relación ya existe, retorna la existente sin duplicar.
        """
        registro = self.get_object()
        if not registro:
            raise NotFound()

        hashtag_id = request.data.get('id_catalogo_hashtag')

        if not hashtag_id:
            raise BadRequest({'error': 'id_catalogo_hashtag es requerido'})

        try:
            # Verificar que el hashtag existe y está activo
            from catalogos.models import CatalogoHashTag
            try:
                hashtag = CatalogoHashTag.objects.get(id=hashtag_id, activo=True)
            except CatalogoHashTag.DoesNotExist:
                raise BadRequest({'error': 'Hashtag no encontrado o inactivo'})

            hashtag_registro, created = HashTag_Registro.objects.get_or_create(
                id_catalogo_hashtag_id=hashtag_id,
                id_registro=registro
            )
            serializer = HashTagRegistroSerializer(hashtag_registro)
            
            if created:
                return created_response(data=serializer.data, message='Hashtag agregado correctamente')
            else:
                return ok_response(data=serializer.data, message='El hashtag ya estaba asociado a este registro')
        except BadRequest:
            raise
        except Exception as e:
            raise BadRequest({'error': str(e)})

    @action(detail=True, methods=['post'])
    def remover_hashtag(self, request, pk=None):
        """Remover un hashtag de un registro"""
        registro = self.get_object()
        if not registro:
            raise NotFound()

        hashtag_id = request.data.get('id_catalogo_hashtag')

        if not hashtag_id:
            raise BadRequest({'error': 'id_catalogo_hashtag es requerido'})

        try:
            deleted_count, _ = HashTag_Registro.objects.filter(
                id_catalogo_hashtag_id=hashtag_id,
                id_registro=registro
            ).delete()
            if deleted_count > 0:
                return ok_response(data=None, message='Hashtag removido correctamente')
            raise NotFound()
        except Exception as e:
            raise BadRequest({'error': str(e)})


class HashTagRegistroViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar la relación entre hashtags y registros.
    """
    queryset = HashTag_Registro.objects.all()
    serializer_class = HashTagRegistroSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = HashTagRegistroFilter
    ordering = ['-created_at']

    def get_object(self):
        """Obtiene un objeto con manejo de excepciones"""
        try:
            obj_id = self.kwargs.get('pk')
            obj = self.get_queryset().get(pk=obj_id)
            return obj
        except ObjectDoesNotExist:
            return None

    def list(self, request, *args, **kwargs):
        """Lista relaciones hashtag-registro"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Obtiene una relación específica"""
        instance = self.get_object()
        if not instance:
            return Response(
                {'error': 'Relación no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """Crear una nueva relación"""
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        """Eliminar una relación"""
        instance = self.get_object()
        if not instance:
            return Response(
                {'error': 'Relación no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        instance.delete()
        return Response(
            {'mensaje': 'Relación eliminada correctamente'},
            status=status.HTTP_204_NO_CONTENT
        )
