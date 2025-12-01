from rest_framework import serializers
from catalogos.models import CatalogoHashTag


class CatalogoHashTagSerializer(serializers.ModelSerializer):
    """Serializador completo para CatalogoHashTag"""
    class Meta:
        model = CatalogoHashTag
        fields = '__all__'


class CatalogoHashTagListSerializer(serializers.ModelSerializer):
    """Serializador para listar hashtags"""
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = CatalogoHashTag
        fields = [
            'id',
            'descripcion',
            'activo',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class CatalogoHashTagCreateSerializer(serializers.ModelSerializer):
    """Serializador para crear hashtags"""
    class Meta:
        model = CatalogoHashTag
        fields = [
            'descripcion',
            'activo'
        ]
        extra_kwargs = {
            'activo': {'default': True},
        }

    def create(self, validated_data):
        hashtag = CatalogoHashTag.objects.create(**validated_data)
        return hashtag


class CatalogoHashTagUpdateSerializer(serializers.ModelSerializer):
    """Serializador para actualizar hashtags"""
    class Meta:
        model = CatalogoHashTag
        fields = [
            'descripcion',
            'activo'
        ]
