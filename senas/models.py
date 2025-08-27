from django.db import models

class Alumno(models.Model):
    nombre = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    contrasena = models.CharField(max_length=50)  # O mejor usar hash si es sensible

    def __str__(self):
        return self.nombre

# Create your models here.
