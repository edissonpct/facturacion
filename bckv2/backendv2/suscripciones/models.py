from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F, Q


class Modulo(models.Model):
    codigo = models.SlugField(
        "código",
        max_length=50,
        unique=True,
    )

    nombre = models.CharField(
        "nombre",
        max_length=100,
    )

    descripcion = models.TextField(
        "descripción",
        blank=True,
    )

    activo = models.BooleanField(
        "activo",
        default=True,
    )

    orden = models.PositiveIntegerField(
        "orden",
        default=0,
    )

    class Meta:
        verbose_name = "módulo"
        verbose_name_plural = "módulos"
        ordering = ("orden", "nombre")

    def __str__(self) -> str:
        return self.nombre


class Plan(models.Model):
    nombre = models.CharField(
        "nombre",
        max_length=100,
        unique=True,
    )

    descripcion = models.TextField(
        "descripción",
        blank=True,
    )

    precio_mensual = models.DecimalField(
        "precio mensual",
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    precio_anual = models.DecimalField(
        "precio anual",
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    activo = models.BooleanField(
        "activo",
        default=True,
    )

    orden = models.PositiveIntegerField(
        "orden",
        default=0,
    )

    modulos = models.ManyToManyField(
        Modulo,
        through="PlanModulo",
        related_name="planes",
        verbose_name="módulos",
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
        verbose_name = "plan"
        verbose_name_plural = "planes"
        ordering = ("orden", "precio_mensual")

    def __str__(self) -> str:
        return self.nombre


class PlanModulo(models.Model):
    plan = models.ForeignKey(
        Plan,
        on_delete=models.CASCADE,
        related_name="modulos_asignados",
        verbose_name="plan",
    )

    modulo = models.ForeignKey(
        Modulo,
        on_delete=models.PROTECT,
        related_name="asignaciones_planes",
        verbose_name="módulo",
    )

    activo = models.BooleanField(
        "activo",
        default=True,
    )

    class Meta:
        verbose_name = "módulo del plan"
        verbose_name_plural = "módulos de los planes"
        ordering = ("plan", "modulo")

        constraints = [
            models.UniqueConstraint(
                fields=("plan", "modulo"),
                name="unico_modulo_por_plan",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.plan.nombre} - {self.modulo.nombre}"

class PlanLimite(models.Model):
    class Tipo(models.TextChoices):
        USUARIOS = "usuarios", "Usuarios"
        SUCURSALES = "sucursales", "Sucursales"
        DOCUMENTOS_MENSUALES = (
            "documentos_mensuales",
            "Documentos mensuales",
        )

    plan = models.ForeignKey(
        Plan,
        on_delete=models.CASCADE,
        related_name="limites",
        verbose_name="plan",
    )

    tipo = models.CharField(
        "tipo de límite",
        max_length=30,
        choices=Tipo.choices,
    )

    cantidad = models.PositiveIntegerField(
        "cantidad",
        blank=True,
        null=True,
        help_text="Dejar vacío para indicar que no existe límite.",
    )

    class Meta:
        verbose_name = "límite del plan"
        verbose_name_plural = "límites de los planes"
        ordering = ("plan", "tipo")

        constraints = [
            models.UniqueConstraint(
                fields=("plan", "tipo"),
                name="unico_tipo_limite_por_plan",
            ),
        ]

    def __str__(self) -> str:
        valor = (
            "Sin límite"
            if self.cantidad is None
            else str(self.cantidad)
        )

        return (
            f"{self.plan.nombre} - "
            f"{self.get_tipo_display()}: {valor}"
        )

class Suscripcion(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente"
        PRUEBA = "prueba", "Periodo de prueba"
        ACTIVA = "activa", "Activa"
        SUSPENDIDA = "suspendida", "Suspendida"
        CANCELADA = "cancelada", "Cancelada"
        VENCIDA = "vencida", "Vencida"

    class CicloFacturacion(models.TextChoices):
        MENSUAL = "mensual", "Mensual"
        ANUAL = "anual", "Anual"

    empresa = models.ForeignKey(
        "empresas.Empresa",
        on_delete=models.CASCADE,
        related_name="suscripciones",
        verbose_name="empresa",
    )

    plan = models.ForeignKey(
        Plan,
        on_delete=models.PROTECT,
        related_name="suscripciones",
        verbose_name="plan",
    )

    estado = models.CharField(
        "estado",
        max_length=12,
        choices=Estado.choices,
        default=Estado.PENDIENTE,
    )

    ciclo_facturacion = models.CharField(
        "ciclo de facturación",
        max_length=10,
        choices=CicloFacturacion.choices,
        default=CicloFacturacion.MENSUAL,
    )

    precio_contratado = models.DecimalField(
        "precio contratado",
        max_digits=10,
        decimal_places=2,
    )

    fecha_inicio = models.DateField(
        "fecha de inicio",
    )

    fecha_fin = models.DateField(
        "fecha de finalización",
        blank=True,
        null=True,
    )

    renovacion_automatica = models.BooleanField(
        "renovación automática",
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
        verbose_name = "suscripción"
        verbose_name_plural = "suscripciones"
        ordering = ("-fecha_inicio", "-id")

        constraints = [
            models.CheckConstraint(
                condition=Q(precio_contratado__gte=0),
                name="suscripcion_precio_no_negativo",
            ),
            models.CheckConstraint(
                condition=(
                    Q(fecha_fin__isnull=True)
                    | Q(fecha_fin__gte=F("fecha_inicio"))
                ),
                name="suscripcion_fechas_validas",
            ),
            models.UniqueConstraint(
                fields=("empresa",),
                condition=Q(
                    estado__in=(
                        "pendiente",
                        "prueba",
                        "activa",
                        "suspendida",
                    )
                ),
                name="unica_suscripcion_vigente_por_empresa",
            ),
        ]

    def clean(self):
        super().clean()

        if (
            self.fecha_inicio
            and self.fecha_fin
            and self.fecha_fin < self.fecha_inicio
        ):
            raise ValidationError(
                {
                    "fecha_fin": (
                        "La fecha de finalización no puede ser "
                        "anterior a la fecha de inicio."
                    )
                }
            )

    def __str__(self) -> str:
        return (
            f"{self.empresa.razon_social} - "
            f"{self.plan.nombre} - "
            f"{self.get_estado_display()}"
        )