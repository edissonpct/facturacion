from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


username_validator = RegexValidator(
    regex=r"^[\w.-]+$",
    message=(
        "El nombre de usuario solo puede contener letras, números, "
        "puntos, guiones y guiones bajos."
    ),
)


class Usuario(AbstractUser):
    username = models.CharField(
        "nombre de usuario",
        max_length=150,
        unique=True,
        validators=[username_validator],
        help_text=(
            "Requerido. Máximo 150 caracteres. "
            "Puede contener letras, números, puntos, guiones y guiones bajos."
        ),
        error_messages={
            "unique": "Ya existe un usuario con este nombre de usuario.",
        },
    )

    email = models.EmailField(
        "correo electrónico",
        unique=True,
        error_messages={
            "unique": "Ya existe un usuario con este correo electrónico.",
        },
    )

    telefono = models.CharField(
        "teléfono",
        max_length=20,
        blank=True,
    )

    class Meta:
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"

    def __str__(self) -> str:
        return self.username