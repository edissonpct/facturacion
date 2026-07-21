from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Q

validador_ruc = RegexValidator(
    regex=r"^\d{13}$",
    message="El RUC debe contener exactamente 13 dígitos.",
)

class Empresa(models.Model):
    ruc = models.CharField(
        "RUC",
        max_length=13,
        unique=True,
        validators=[validador_ruc],
        error_messages={
            "unique": "Ya existe una empresa registrada con este RUC.",
        },
    )

    razon_social = models.CharField(
        "razón social",
        max_length=200,
    )

    nombre_comercial = models.CharField(
        "nombre comercial",
        max_length=200,
        blank=True,
    )

    email = models.EmailField(
        "correo electrónico",
        blank=True,
    )

    telefono = models.CharField(
        "teléfono",
        max_length=20,
        blank=True,
    )

    activo = models.BooleanField(
        "activo",
        default=True,
    )

    fecha_creacion = models.DateTimeField(
        "fecha de creación",
        auto_now_add=True,
    )

    fecha_actualizacion = models.DateTimeField(
        "fecha de actualización",
        auto_now=True,
    )

    class Meta:
        verbose_name = "empresa"
        verbose_name_plural = "empresas"
        ordering = ("razon_social",)

    def __str__(self) -> str:
        return f"{self.razon_social} - {self.ruc}"


validador_codigo_sucursal = RegexValidator(
    regex=r"^\d{3}$",
    message="El código de la sucursal debe contener exactamente 3 dígitos.",
)


class Sucursal(models.Model):
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name="sucursales",
        verbose_name="empresa",
    )

    codigo = models.CharField(
        "código",
        max_length=3,
        validators=[validador_codigo_sucursal],
    )

    nombre = models.CharField(
        "nombre",
        max_length=150,
    )

    direccion = models.CharField(
        "dirección",
        max_length=255,
    )

    telefono = models.CharField(
        "teléfono",
        max_length=20,
        blank=True,
    )

    email = models.EmailField(
        "correo electrónico",
        blank=True,
    )

    es_matriz = models.BooleanField(
        "es matriz",
        default=False,
    )

    activo = models.BooleanField(
        "activo",
        default=True,
    )

    fecha_creacion = models.DateTimeField(
        "fecha de creación",
        auto_now_add=True,
    )

    fecha_actualizacion = models.DateTimeField(
        "fecha de actualización",
        auto_now=True,
    )

    class Meta:
        verbose_name = "sucursal"
        verbose_name_plural = "sucursales"
        ordering = ("nombre",)

        constraints = [
            models.UniqueConstraint(
                fields=("empresa", "codigo"),
                name="unica_sucursal_codigo_por_empresa",
            ),
            models.UniqueConstraint(
                fields=("empresa",),
                condition=Q(es_matriz=True),
                name="unica_sucursal_matriz_por_empresa",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.empresa.razon_social} - {self.codigo} - {self.nombre}"