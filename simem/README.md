# Estructura del Proyecto SIMEM

## Descripción General
SIMEM es un Sistema Integral de Monitoreo construido con Django y Django REST Framework que organiza la funcionalidad en 4 aplicaciones principales:

## Estructura de Aplicaciones

### 1. **api/** (Aplicación Principal)
- Centraliza las rutas de la API REST
- Coordina el enrutamiento de todos los viewsets
- **Archivos:**
  - `urls.py` - Router para todos los endpoints

### 2. **usuarios/** (Gestión de Usuarios)
- Manejo de autenticación y autorización
- Modelo personalizado que extiende AbstractUser
- **Archivos:**
  - `models.py` - Modelo Usuarios
  - `serializers.py` - Serializers (Simple, List, Retrieve, Create, Update)
  - `viewsets.py` - UsuariosViewSet con CRUD completo
  - `filters.py` - UsuariosFilter
  - `admin.py` - Configuración del admin

### 3. **catalogos/** (Catálogos del Sistema)
- Gestión de datos maestros (HashTags)
- **Archivos:**
  - `models.py` - Modelo CatalogoHashTag
  - `serializers.py` - Serializers
  - `viewsets.py` - CatalogoHashTagViewSet
  - `filters.py` - CatalogoHashTagFilter
  - `admin.py` - Configuración del admin

### 4. **movilizaciones/** (Movilizaciones y Registros)
- Gestión de expedientes, registros y relaciones
- **Archivos:**
  - `models.py` - Modelos: Expedientes, Registro, HashTag_Registro
  - `serializers.py` - Serializers para cada modelo
  - `viewsets.py` - ViewSets: ExpedientesViewSet, RegistroViewSet, HashTagRegistroViewSet
  - `filters.py` - Filters: ExpedientesFilter, RegistroFilter, HashTagRegistroFilter
  - `admin.py` - Configuración del admin

## Modelos de Datos

### Usuarios
- Extiende AbstractUser de Django
- Campos adicionales: rut, apellido_paterno, apellido_materno, numero_empleado

### CatalogoHashTag
- id, descripcion, activo, created_at, updated_at

### Expedientes
- id, usuarios_id (FK), asunto, fecha_evento, descripcion, created_at, updated_at

### Registro
- id, expedientes_id (FK), creado_por (FK), ubicacion, descripcion, url_foto, fecha, hora, activo, created_at, updated_at

### HashTag_Registro
- id, id_catalogo_hashtag (FK), id_registro (FK), created_at, updated_at

## Endpoints de la API

### Usuarios
- `GET/POST /api/v1/usuarios/` - Listar/Crear usuarios
- `GET/PUT/PATCH/DELETE /api/v1/usuarios/{id}/` - Detalle/Actualizar/Eliminar
- `GET /api/v1/usuarios/me/` - Usuario actual
- `GET /api/v1/usuarios/activos/` - Usuarios activos
- `POST /api/v1/usuarios/{id}/cambiar_contraseña/` - Cambiar contraseña

### Catálogos (HashTags)
- `GET/POST /api/v1/catalogos/hashtags/` - Listar/Crear hashtags
- `GET/PUT/PATCH/DELETE /api/v1/catalogos/hashtags/{id}/` - Detalle/Actualizar/Eliminar
- `GET /api/v1/catalogos/hashtags/activos/` - Hashtags activos

### Expedientes
- `GET/POST /api/v1/expedientes/` - Listar/Crear expedientes
- `GET/PUT/PATCH/DELETE /api/v1/expedientes/{id}/` - Detalle/Actualizar/Eliminar
- `GET /api/v1/expedientes/{id}/registros/` - Registros de un expediente

### Registros
- `GET/POST /api/v1/registros/` - Listar/Crear registros
- `GET/PUT/PATCH/DELETE /api/v1/registros/{id}/` - Detalle/Actualizar/Eliminar
- `POST /api/v1/registros/{id}/agregar_hashtag/` - Agregar hashtag
- `DELETE /api/v1/registros/{id}/remover_hashtag/` - Remover hashtag

### Relaciones HashTag-Registro
- `GET/POST /api/v1/hashtag-registros/` - Listar/Crear relaciones
- `GET/DELETE /api/v1/hashtag-registros/{id}/` - Detalle/Eliminar

## Características Principales

### Filtrado
- Filtros configurados en cada aplicación usando `django_filters`
- Búsqueda por múltiples campos usando SearchFilter
- Ordenamiento personalizado

### Serializers
- Serializers específicos por acción (List, Retrieve, Create, Update)
- Validación de datos personalizada
- Campos anidados para relaciones

### Permisos
- Basado en IsAuthenticated
- Control por usuario (superuser vs usuario normal)
- Creación de usuarios sin autenticación

### Paginación
- Paginación por número de página
- 20 items por página

## Configuración de Django REST Framework

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}
```

## Instalación y Configuración

1. Instalar dependencias:
```bash
pipenv install
source /path/to/virtualenv/bin/activate
```

2. Ejecutar migraciones:
```bash
python manage.py makemigrations
python manage.py migrate
```

3. Crear superusuario:
```bash
python manage.py createsuperuser
```

4. Ejecutar servidor:
```bash
python manage.py runserver
```

5. Acceder a la API:
- Documentación: http://localhost:8000/api/docs/
- Admin: http://localhost:8000/admin/
- API: http://localhost:8000/api/v1/
