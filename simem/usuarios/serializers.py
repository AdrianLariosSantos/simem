from rest_framework import serializers
from usuarios.models import Usuarios
from django.contrib.auth.models import Group


class UsuariosSerializer(serializers.ModelSerializer):
    """Serializador completo para el modelo Usuarios"""
    class Meta:
        model = Usuarios
        fields = '__all__'


class UsuariosListSerializer(serializers.ModelSerializer):
    """Serializador para listar usuarios"""
    created_at = serializers.DateTimeField(source='date_joined', read_only=True)
    nombre_completo = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = Usuarios
        fields = [
            'id',
            'nombre_completo',
            'username',
            'first_name',
            'apellido_paterno',
            'apellido_materno',
            'email',
            'is_active',
            'is_superuser',
            'is_staff',
            'numero_empleado',
            'created_at',
            'role',
            'permissions',
        ]
        extra_kwargs = {
            'is_superuser': {'default': False},
            'is_active': {'default': True},
        }

    def get_nombre_completo(self, obj):
        return f'{obj.first_name} {obj.apellido_paterno} {obj.apellido_materno}'

    def get_role(self, obj):
        return obj.groups.first().name if obj.groups.exists() else None

    def get_permissions(self, obj):
        return list(obj.get_all_permissions())


class UsuariosRetrieveSerializer(serializers.ModelSerializer):
    """Serializador para obtener detalles de un usuario"""
    created_at = serializers.DateTimeField(source='date_joined', read_only=True)
    nombre_completo = serializers.SerializerMethodField()

    class Meta:
        model = Usuarios
        fields = [
            'id',
            'nombre_completo',
            'username',
            'first_name',
            'apellido_paterno',
            'apellido_materno',
            'email',
            'numero_empleado',
            'is_active',
            'is_superuser',
            'is_staff',
            'created_at',
        ]
        extra_kwargs = {
            'is_superuser': {'default': False},
            'is_active': {'default': True},
        }

    def get_nombre_completo(self, obj):
        return f'{obj.first_name} {obj.apellido_paterno} {obj.apellido_materno}'


class UsuariosCreateSerializer(serializers.ModelSerializer):
    """Serializador para crear usuarios"""
    created_at = serializers.DateTimeField(source='date_joined', read_only=True)
    role = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Usuarios
        fields = [
            'username',
            'first_name',
            'apellido_paterno',
            'apellido_materno',
            'email',
            'numero_empleado',
            'password',
            'is_active',
            'is_superuser',
            'created_at',
            'role',
        ]
        extra_kwargs = {
            'is_superuser': {'default': False},
            'is_active': {'default': True},
        }

    def create(self, validated_data):
        role_name = validated_data.pop('role', None)
        password = validated_data.pop('password')
        
        user = Usuarios.objects.create_user(
            password=password,
            **validated_data
        )
        user.is_staff = False
        user.save()

        if role_name:
            group, _ = Group.objects.get_or_create(name=role_name)
            user.groups.add(group)

        return user


class UsuariosUpdateSerializer(serializers.ModelSerializer):
    """Serializador para actualizar usuarios"""
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Usuarios
        fields = [
            'username',
            'first_name',
            'apellido_paterno',
            'apellido_materno',
            'email',
            'numero_empleado',
            'is_active',
            'is_superuser',
            'password',
            'confirm_password',
        ]
        extra_kwargs = {
            'is_superuser': {'default': False},
            'is_active': {'default': True},
        }

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password or confirm_password:
            if password != confirm_password:
                raise serializers.ValidationError("Las contraseñas no coinciden")
        return data

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        validated_data.pop('confirm_password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance
