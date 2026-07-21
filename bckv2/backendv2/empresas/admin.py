from django.contrib import admin

from .models import Empresa, Sucursal


class SucursalInline(admin.TabularInline):
    model = Sucursal
    extra = 0

    fields = (
        "codigo",
        "nombre",
        "direccion",
        "telefono",
        "email",
        "es_matriz",
        "activo",
    )


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = (
        "ruc",
        "razon_social",
        "nombre_comercial",
        "activo",
        "fecha_creacion",
    )

    search_fields = (
        "ruc",
        "razon_social",
        "nombre_comercial",
    )

    list_filter = (
        "activo",
        "fecha_creacion",
    )

    ordering = (
        "razon_social",
    )

    readonly_fields = (
        "fecha_creacion",
        "fecha_actualizacion",
    )

    inlines = (
        SucursalInline,
    )


@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    list_display = (
        "codigo",
        "nombre",
        "empresa",
        "es_matriz",
        "activo",
    )

    search_fields = (
        "codigo",
        "nombre",
        "empresa__ruc",
        "empresa__razon_social",
    )

    list_filter = (
        "es_matriz",
        "activo",
        "empresa",
    )

    ordering = (
        "empresa",
        "codigo",
    )

    autocomplete_fields = (
        "empresa",
    )

    readonly_fields = (
        "fecha_creacion",
        "fecha_actualizacion",
    )