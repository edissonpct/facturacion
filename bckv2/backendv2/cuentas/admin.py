from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from .models import Usuario

@admin.register(Usuario)
#UserAdmin --> configuración visual y funcional del panel admin
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
    # Campos al crear usuario desde el admin
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
        "is_staff",
        "is_active",
    )

    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
        "groups",
    )

    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
    )

    ordering = ("username",)