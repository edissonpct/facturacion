from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Membresia, MembresiaSucursal, Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            "Información adicional",
            {
                "fields": (
                    "telefono",
                ),
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Información adicional",
            {
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "telefono",
                ),
            },
        ),
    )

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "telefono",
        "is_staff",
        "is_active",
    )

    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
    )

    list_filter = (
        "is_active",
        "is_staff",
        "is_superuser",
        "groups",
    )

    ordering = ("username",)


class MembresiaSucursalInline(admin.TabularInline):
    model = MembresiaSucursal
    extra = 0

    autocomplete_fields = (
        "sucursal",
    )

    fields = (
        "sucursal",
        "es_principal",
        "fecha_asignacion",
    )

    readonly_fields = (
        "fecha_asignacion",
    )


@admin.register(Membresia)
class MembresiaAdmin(admin.ModelAdmin):
    list_display = (
        "usuario",
        "empresa",
        "rol",
        "estado",
        "fecha_invitacion",
        "fecha_aceptacion",
    )

    search_fields = (
        "usuario__username",
        "usuario__email",
        "usuario__first_name",
        "usuario__last_name",
        "empresa__ruc",
        "empresa__razon_social",
        "empresa__nombre_comercial",
    )

    list_filter = (
        "rol",
        "estado",
        "empresa",
        "fecha_invitacion",
    )

    autocomplete_fields = (
        "usuario",
        "empresa",
    )

    readonly_fields = (
        "fecha_invitacion",
        "fecha_actualizacion",
    )

    ordering = (
        "empresa",
        "usuario",
    )

    inlines = (
        MembresiaSucursalInline,
    )


@admin.register(MembresiaSucursal)
class MembresiaSucursalAdmin(admin.ModelAdmin):
    list_display = (
        "membresia",
        "sucursal",
        "es_principal",
        "fecha_asignacion",
    )

    search_fields = (
        "membresia__usuario__username",
        "membresia__usuario__email",
        "membresia__empresa__ruc",
        "membresia__empresa__razon_social",
        "sucursal__codigo",
        "sucursal__nombre",
    )

    list_filter = (
        "es_principal",
        "membresia__empresa",
        "sucursal",
    )

    autocomplete_fields = (
        "membresia",
        "sucursal",
    )

    readonly_fields = (
        "fecha_asignacion",
    )

    ordering = (
        "membresia",
        "sucursal",
    )