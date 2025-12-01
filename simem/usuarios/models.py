from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuarios(AbstractUser):
    """Modelo personalizado de Usuario que extiende AbstractUser"""
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    numero_empleado = models.IntegerField(unique=True, null=True, blank=True)
    
    class Meta:
        db_table = 'usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f"{self.first_name} {self.apellido_paterno} {self.apellido_materno}"

    @property
    def nombre_completo(self):
        return f"{self.first_name} {self.apellido_paterno} {self.apellido_materno}"
