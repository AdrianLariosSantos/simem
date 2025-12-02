from rest_framework import serializers
from movilizaciones.models import Expedientes, Registro, HashTag_Registro
from catalogos.models import CatalogoHashTag


class ExpedientesSerializer(serializers.ModelSerializer):
    """Serializador completo para Expedientes"""
    class Meta:
        model = Expedientes
        fields = '__all__'


class ExpedientesListSerializer(serializers.ModelSerializer):
    """Serializador para listar expedientes"""
    usuario_nombre = serializers.CharField(source='usuarios_id.nombre_completo', read_only=True)
    registros_count = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(read_only=True)
    fecha_evento = serializers.DateTimeField(format='%d/%m/%Y', read_only=True)

    class Meta:
        model = Expedientes
        fields = [
            'id',
            'usuarios_id',
            'usuario_nombre',
            'asunto',
            'fecha_evento',
            'activo',
            'created_at',
            'updated_at',
            'registros_count'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_registros_count(self, obj):
        return obj.registros.count()


class ExpedientesDetailSerializer(serializers.ModelSerializer):
    """Serializador detallado para expedientes"""
    usuario_nombre = serializers.CharField(source='usuarios_id.nombre_completo', read_only=True)
    registros_count = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(read_only=True)
    fecha_evento = serializers.DateTimeField(format='%d/%m/%Y', read_only=True)

    class Meta:
        model = Expedientes
        fields = [
            'id',
            'usuarios_id',
            'usuario_nombre',
            'asunto',
            'fecha_evento',
            'registros_count',
            'created_at',
            'activo',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_registros_count(self, obj):
        return obj.registros.count()


class ExpedientesCreateSerializer(serializers.ModelSerializer):
    """Serializador para crear expedientes"""
    class Meta:
        model = Expedientes
        fields = [
            'asunto',
            'fecha_evento',
            'activo',

        ]

    def create(self, validated_data):
        expediente = Expedientes.objects.create(**validated_data)
        return expediente


class HashTagRegistroSerializer(serializers.ModelSerializer):
    """Serializador para la relación HashTag_Registro"""
    hashtag_descripcion = serializers.CharField(source='id_catalogo_hashtag.descripcion', read_only=True)

    class Meta:
        model = HashTag_Registro
        fields = [
            'id',
            'id_catalogo_hashtag',
            'hashtag_descripcion',
            'id_registro',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class RegistroSerializer(serializers.ModelSerializer):
    """Serializador para listar registros"""
    usuario_nombre = serializers.CharField(source='creado_por.nombre_completo', read_only=True)
    hashtags = HashTagRegistroSerializer(source='hashtag_registros', many=True, read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Registro
        fields = [
            'id',
            'expedientes_id',
            'creado_por',
            'usuario_nombre',
            'ubicacion',
            'descripcion',
            'url_foto',
            'fecha',
            'hora',
            'activo',
            'hashtags',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['fecha', 'hora', 'created_at', 'updated_at']


class RegistroDetailSerializer(serializers.ModelSerializer):
    """Serializador detallado para registros"""
    usuario_nombre = serializers.CharField(source='creado_por.nombre_completo', read_only=True)
    expediente = ExpedientesListSerializer(source='expedientes_id', read_only=True)
    hashtags = HashTagRegistroSerializer(source='hashtag_registros', many=True, read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Registro
        fields = [
            'id',
            'expedientes_id',
            'expediente',
            'creado_por',
            'usuario_nombre',
            'ubicacion',
            'descripcion',
            'url_foto',
            'fecha',
            'hora',
            'activo',
            'hashtags',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['fecha', 'hora', 'created_at', 'updated_at']


class RegistroCreateSerializer(serializers.ModelSerializer):
    """Serializador para crear registros"""
    class Meta:
        model = Registro
        fields = [
            'expedientes_id',
            'ubicacion',
            'descripcion',
            'url_foto',
            'activo'
        ]
        extra_kwargs = {
            'activo': {'default': True},
        }

    def create(self, validated_data):
        registro = Registro.objects.create(**validated_data)
        return registro


class RegistroUpdateSerializer(serializers.ModelSerializer):
    """Serializador para actualizar registros"""
    class Meta:
        model = Registro
        fields = [
            'ubicacion',
            'descripcion',
            'url_foto',
            'activo'
        ]
