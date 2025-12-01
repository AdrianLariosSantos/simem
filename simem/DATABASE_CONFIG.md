# Configuración de Base de Datos PostgreSQL

## Prerequisitos

1. Tener PostgreSQL instalado en tu sistema
2. Tener creada una base de datos

## Pasos para Configurar

### 1. Copiar el archivo `.env.example`

```bash
cp .env.example .env
```

### 2. Editar el archivo `.env` con tus credenciales

```bash
# Database Configuration
DB_ENGINE=django.db.backends.postgresql
DB_NAME=simem_db              # Nombre de tu base de datos
DB_USER=postgres              # Usuario de PostgreSQL
DB_PASSWORD=your_password     # Tu contraseña
DB_HOST=localhost             # Host del servidor (localhost si es local)
DB_PORT=5432                  # Puerto de PostgreSQL (5432 por defecto)

# Django Settings
DEBUG=True
SECRET_KEY=tu-clave-secreta
ALLOWED_HOSTS=localhost,127.0.0.1

# Application Settings
ENVIRONMENT=development
```

### 3. Crear la base de datos en PostgreSQL

```sql
-- Conectarse a PostgreSQL
psql -U postgres

-- Crear la base de datos
CREATE DATABASE simem_db;

-- Ver las bases de datos
\l

-- Salir
\q
```

### 4. Ejecutar las migraciones

```bash
# Activar el entorno virtual
source /path/to/venv/bin/activate

# Ejecutar makemigrations
python manage.py makemigrations

# Ejecutar migrate
python manage.py migrate
```

### 5. Crear un superusuario

```bash
python manage.py createsuperuser
```

### 6. Iniciar el servidor

```bash
python manage.py runserver
```

## Notas Importantes

- **NUNCA** commits el archivo `.env` a git
- El archivo `.env` contiene información sensible
- Siempre usa `.env.example` como plantilla
- En producción, usa variables de entorno del sistema

## Alternativas para el HOST

- **localhost o 127.0.0.1**: Para conexión local
- **IP del servidor**: Para conexión remota (ej: 192.168.1.100)
- **Dominio**: Para servidor en la nube (ej: db.example.com)

## Troubleshooting

### Error: "could not translate host name "localhost" to address"
- Verifica que PostgreSQL esté corriendo
- En Linux/Mac: `sudo systemctl start postgresql`
- En Windows: Iniciar el servicio PostgreSQL desde Services

### Error: "FATAL: password authentication failed for user "postgres""
- Verifica que la contraseña en `.env` sea correcta
- Asegúrate de usar la contraseña del usuario postgres

### Error: "FATAL: database "simem_db" does not exist"
- Crea la base de datos ejecutando: `CREATE DATABASE simem_db;`

## Conexión Exitosa

Una vez configurado correctamente, deberías ver en el log:
```
Performing system checks...

System check identified no issues (0 silenced).
November 27, 2025 - 13:00:00
Django version 5.2.8
Database: PostgreSQL
Server is running at http://127.0.0.1:8000/
```
