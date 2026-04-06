from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    empresa = models.ForeignKey(
        'organizacion.Empresa',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='usuarios'
    )

    def __str__(self):
        return self.username