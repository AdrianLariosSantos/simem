from django.db import models


class CatalogoHashTag(models.Model):
    """Modelo para el catálogo de hashtags"""
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=255)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'catalogo_hashtag'
        verbose_name = 'Catálogo Hashtag'
        verbose_name_plural = 'Catálogos Hashtag'

    def __str__(self):
        return self.descripcion
