from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.conf import settings



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

class Membresia(models.Model):
    class Rol(models.TextChoices):
        PROPIETARIO = "propietario", "Propietario"
        ADMINISTRADOR = "administrador", "Administrador"
        CONTADOR_EXTERNO = "contador_externo", "Contador externo"
        EMPLEADO = "empleado", "Empleado"
        CONSULTA = "consulta", "Solo consulta"

    class Estado(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente"
        ACTIVA = "activa", "Activa"
        SUSPENDIDA = "suspendida", "Suspendida"
        REVOCADA = "revocada", "Revocada"

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="membresias",
        verbose_name="usuario",
    )

    empresa = models.ForeignKey(
        "empresas.Empresa",
        on_delete=models.CASCADE,
        related_name="membresias",
        verbose_name="empresa",
    )

    rol = models.CharField(
        "rol",
        max_length=20,
        choices=Rol.choices,
        default=Rol.EMPLEADO,
    )

    estado = models.CharField(
        "estado",
        max_length=12,
        choices=Estado.choices,
        default=Estado.PENDIENTE,
    )

    fecha_invitacion = models.DateTimeField(
        "fecha de invitación",
        auto_now_add=True,
    )

    fecha_aceptacion = models.DateTimeField(
        "fecha de aceptación",
        blank=True,
        null=True,
    )

    fecha_actualizacion = models.DateTimeField(
        "fecha de actualización",
        auto_now=True,
    )

    class Meta:
        verbose_name = "membresía"
        verbose_name_plural = "membresías"
        ordering = ("empresa", "usuario")

        constraints = [
            models.UniqueConstraint(
                fields=("usuario", "empresa"),
                name="unica_membresia_usuario_empresa",
            ),
        ]

    def __str__(self) -> str:
        return (
            f"{self.usuario.username} - "
            f"{self.empresa.razon_social} - "
            f"{self.get_rol_display()}"
        )
    
