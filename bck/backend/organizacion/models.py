from django.db import models

class Empresa(models.Model):
    nombre = models.CharField(max_length=255)
    razonsocial = models.CharField(max_length=255)
    ruc = models.CharField(max_length=13, unique=True)

    def __str__(self):
        return self.nombre