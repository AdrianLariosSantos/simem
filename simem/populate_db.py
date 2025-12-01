#!/usr/bin/env python
"""
Script para popular la base de datos con datos de prueba
"""
import os
import django
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simem.settings')
django.setup()

from usuarios.models import Usuarios
from catalogos.models import CatalogoHashTag
from movilizaciones.models import Expedientes, Registro, HashTag_Registro

def clear_database():
    """Limpiar datos previos (excepto admin)"""
    print("Limpiando datos previos...")
    HashTag_Registro.objects.all().delete()
    Registro.objects.all().delete()
    Expedientes.objects.all().delete()
    CatalogoHashTag.objects.all().delete()
    Usuarios.objects.filter(username__startswith='usuario').delete()
    print("✓ Base de datos limpia")

def create_usuarios():
    """Crear usuarios de prueba"""
    print("\nCreando usuarios...")
    usuarios_data = [
        {'username': 'usuario1', 'email': 'usuario1@simem.com', 'first_name': 'Juan', 'apellido_paterno': 'Pérez', 'apellido_materno': 'López'},
        {'username': 'usuario2', 'email': 'usuario2@simem.com', 'first_name': 'María', 'apellido_paterno': 'García', 'apellido_materno': 'Martínez'},
        {'username': 'usuario3', 'email': 'usuario3@simem.com', 'first_name': 'Carlos', 'apellido_paterno': 'López', 'apellido_materno': 'Rodríguez'},
        {'username': 'usuario4', 'email': 'usuario4@simem.com', 'first_name': 'Ana', 'apellido_paterno': 'Martínez', 'apellido_materno': 'Sánchez'},
        {'username': 'usuario5', 'email': 'usuario5@simem.com', 'first_name': 'Roberto', 'apellido_paterno': 'Rodríguez', 'apellido_materno': 'González'},
    ]
    
    usuarios = []
    for data in usuarios_data:
        usuario = Usuarios.objects.create_user(
            username=data['username'],
            email=data['email'],
            password='password123',
            first_name=data['first_name'],
            apellido_paterno=data['apellido_paterno'],
            apellido_materno=data['apellido_materno'],
        )
        usuarios.append(usuario)
        print(f"  ✓ {usuario.nombre_completo}")
    
    return usuarios

def create_hashtags():
    """Crear hashtags de prueba"""
    print("\nCreando hashtags...")
    hashtags_data = [
        'urgente',
        'seguimiento',
        'completado',
        'pendiente',
        'en_revision',
        'archivado',
        'critico',
        'importante',
        'bajo_prioridad',
        'bloqueado',
    ]
    
    hashtags = []
    for descripcion in hashtags_data:
        hashtag = CatalogoHashTag.objects.create(descripcion=descripcion)
        hashtags.append(hashtag)
        print(f"  ✓ {hashtag.descripcion}")
    
    return hashtags

def create_expedientes(usuarios):
    """Crear expedientes de prueba"""
    print("\nCreando expedientes...")
    expedientes_data = [
        {'asunto': 'Caso de prueba 1', 'descripcion': 'Descripción del caso 1'},
        {'asunto': 'Caso de prueba 2', 'descripcion': 'Descripción del caso 2'},
        {'asunto': 'Caso de prueba 3', 'descripcion': 'Descripción del caso 3'},
        {'asunto': 'Caso de prueba 4', 'descripcion': 'Descripción del caso 4'},
        {'asunto': 'Caso de prueba 5', 'descripcion': 'Descripción del caso 5'},
    ]
    
    expedientes = []
    for i, data in enumerate(expedientes_data):
        usuario = usuarios[i % len(usuarios)]
        expediente = Expedientes.objects.create(
            asunto=data['asunto'],
            descripcion=data['descripcion'],
            usuarios_id=usuario,
            fecha_evento=timezone.now(),
        )
        expedientes.append(expediente)
        print(f"  ✓ {expediente.asunto} - {usuario.nombre_completo}")
    
    return expedientes

def create_registros(expedientes, usuarios):
    """Crear registros de prueba"""
    print("\nCreando registros...")
    registros_data = [
        {'ubicacion': 'https://maps.google.com/maps?q=-33.8688,151.2093&z=15', 'descripcion': 'Primera revisión del expediente', 'url_foto': 'https://images.unsplash.com/photo-1517694712202-14819c9cb6c3?w=400&h=300&fit=crop'},
        {'ubicacion': 'https://maps.google.com/maps?q=-33.8830,151.1935&z=15', 'descripcion': 'Documento agregado', 'url_foto': 'https://images.unsplash.com/photo-1552664730-d307ca884978?w=400&h=300&fit=crop'},
        {'ubicacion': 'https://maps.google.com/maps?q=-33.8747,151.2072&z=15', 'descripcion': 'Cambio de estado', 'url_foto': 'https://images.unsplash.com/photo-1516534775068-bb57a52f4fee?w=400&h=300&fit=crop'},
        {'ubicacion': 'https://maps.google.com/maps?q=-33.8688,151.2093&z=15', 'descripcion': 'Comentario importante', 'url_foto': 'https://images.unsplash.com/photo-1454496522488-7a8e488e8606?w=400&h=300&fit=crop'},
        {'ubicacion': 'https://maps.google.com/maps?q=-33.8730,151.2065&z=15', 'descripcion': 'Validación completada', 'url_foto': 'https://images.unsplash.com/photo-1552664730-d307ca884978?w=400&h=300&fit=crop'},
        {'ubicacion': 'https://maps.google.com/maps?q=-33.8780,151.2100&z=15', 'descripcion': 'Aprobación requerida', 'url_foto': 'https://images.unsplash.com/photo-1517694712202-14819c9cb6c3?w=400&h=300&fit=crop'},
        {'ubicacion': 'https://maps.google.com/maps?q=-33.8850,151.2150&z=15', 'descripcion': 'Datos actualizados', 'url_foto': 'https://images.unsplash.com/photo-1516534775068-bb57a52f4fee?w=400&h=300&fit=crop'},
        {'ubicacion': 'https://maps.google.com/maps?q=-33.8700,151.1950&z=15', 'descripcion': 'Seguimiento programado', 'url_foto': 'https://images.unsplash.com/photo-1454496522488-7a8e488e8606?w=400&h=300&fit=crop'},
        {'ubicacion': 'https://maps.google.com/maps?q=-33.8760,151.2080&z=15', 'descripcion': 'Notificación enviada', 'url_foto': 'https://images.unsplash.com/photo-1552664730-d307ca884978?w=400&h=300&fit=crop'},
        {'ubicacion': 'https://maps.google.com/maps?q=-33.8720,151.2040&z=15', 'descripcion': 'Cierre de expediente', 'url_foto': 'https://images.unsplash.com/photo-1517694712202-14819c9cb6c3?w=400&h=300&fit=crop'},
    ]
    
    registros = []
    for i, data in enumerate(registros_data):
        expediente = expedientes[i % len(expedientes)]
        usuario = usuarios[i % len(usuarios)]
        
        registro = Registro.objects.create(
            expedientes_id=expediente,
            creado_por=usuario,
            descripcion=data['descripcion'],
            ubicacion=data['ubicacion'],
            url_foto=data['url_foto'],
        )
        registros.append(registro)
        print(f"  ✓ Registro {i+1}: {expediente.asunto} - {usuario.nombre_completo}")
    
    return registros

def create_hashtag_registros(registros, hashtags):
    """Crear relaciones hashtag-registro"""
    print("\nCreando relaciones hashtag-registro...")
    for i, registro in enumerate(registros):
        # Asignar 1-3 hashtags aleatorios a cada registro
        num_hashtags = (i % 3) + 1
        for j in range(num_hashtags):
            hashtag = hashtags[(i + j) % len(hashtags)]
            try:
                HashTag_Registro.objects.create(
                    id_registro=registro,
                    id_catalogo_hashtag=hashtag,
                )
            except:
                pass  # Ignorar duplicados
        print(f"  ✓ Registro {i+1} etiquetado")

def main():
    print("=" * 50)
    print("POBLANDO BASE DE DATOS CON DATOS DE PRUEBA")
    print("=" * 50)
    
    try:
        clear_database()
        usuarios = create_usuarios()
        hashtags = create_hashtags()
        expedientes = create_expedientes(usuarios)
        registros = create_registros(expedientes, usuarios)
        create_hashtag_registros(registros, hashtags)
        
        print("\n" + "=" * 50)
        print("✅ BASE DE DATOS POBLADA EXITOSAMENTE")
        print("=" * 50)
        print(f"\nResumen:")
        print(f"  • Usuarios: {Usuarios.objects.filter(is_superuser=False).count()}")
        print(f"  • Hashtags: {CatalogoHashTag.objects.count()}")
        print(f"  • Expedientes: {Expedientes.objects.count()}")
        print(f"  • Registros: {Registro.objects.count()}")
        print(f"  • Relaciones Hashtag-Registro: {HashTag_Registro.objects.count()}")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
