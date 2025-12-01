from django.db import models
from django.contrib.auth import get_user_model
from catalogos.models import CatalogoHashTag

User = get_user_model()


class Expedientes(models.Model):
    """Modelo para gestionar expedientes"""
    id = models.AutoField(primary_key=True)
    usuarios_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expedientes')
    asunto = models.CharField(max_length=255)
    fecha_evento = models.DateTimeField()
    descripcion = models.TextField(null=True, blank=True)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'expedientes'
        verbose_name = 'Expediente'
        verbose_name_plural = 'Expedientes'

    def __str__(self):
        return f"{self.asunto} - {self.fecha_evento}"


class Registro(models.Model):
    """Modelo para registros con relación a expedientes y hashtags"""
    id = models.AutoField(primary_key=True)
    expedientes_id = models.ForeignKey(Expedientes, on_delete=models.CASCADE, related_name='registros')
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='registros_creados')
    ubicacion = models.CharField(max_length=255)
    descripcion = models.TextField(null=True, blank=True)
    url_foto = models.URLField(null=True, blank=True)
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'registro'
        verbose_name = 'Registro'
        verbose_name_plural = 'Registros'

    def __str__(self):
        return f"Registro {self.id} - {self.ubicacion}"


class HashTag_Registro(models.Model):
    """Modelo de relación muchos a muchos entre Hashtags y Registros"""
    id = models.AutoField(primary_key=True)
    id_catalogo_hashtag = models.ForeignKey(CatalogoHashTag, on_delete=models.CASCADE, related_name='hashtag_registros')
    id_registro = models.ForeignKey(Registro, on_delete=models.CASCADE, related_name='hashtag_registros')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hashtag_registro'
        verbose_name = 'Hashtag Registro'
        verbose_name_plural = 'Hashtag Registros'
        unique_together = ('id_catalogo_hashtag', 'id_registro')

    def __str__(self):
        return f"{self.id_catalogo_hashtag} - {self.id_registro}"
