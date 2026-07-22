from djoser.serializers import (
    UserCreatePasswordRetypeSerializer,
    UserSerializer,
)
from rest_framework import serializers

from .models import Usuario
from empresas.models import Sucursal
from .models import Membresia



class UsuarioCrearSerializer(UserCreatePasswordRetypeSerializer):
    """
    Se utiliza para registrar un usuario mediante:

    POST /api/auth/users/
    """

    class Meta(UserCreatePasswordRetypeSerializer.Meta):
        model = Usuario
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "telefono",
            "password",
            "re_password",
        )
        read_only_fields = ("id",)


class UsuarioPublicoSerializer(UserSerializer):
    """
    Información limitada que puede mostrarse de otros usuarios.

    No expone:
    - correo electrónico;
    - teléfono;
    - permisos;
    - indicadores de staff o superusuario.
    """

    class Meta(UserSerializer.Meta):
        model = Usuario
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "foto",
        )
        read_only_fields = fields


class UsuarioActualSerializer(UserSerializer):
    """
    Perfil completo del usuario autenticado.

    Se utiliza principalmente en:

    GET   /api/auth/users/me/
    PATCH /api/auth/users/me/
    """

    class Meta(UserSerializer.Meta):
        model = Usuario
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "telefono",
        )
        read_only_fields = (
            "id",
            "username",
        )

class SucursalDisponibleSerializer(serializers.ModelSerializer):
    """
    Información resumida de una sucursal activa.
    """

    class Meta:
        model = Sucursal
        fields = (
            "id",
            "codigo",
            "nombre",
            "es_matriz",
        )
        read_only_fields = fields


class EmpresaDisponibleSerializer(serializers.ModelSerializer):
    """
    Representa una membresía activa junto con los datos
    de la empresa y sus sucursales disponibles.
    """

    empresa_id = serializers.IntegerField(
        source="empresa.id",
        read_only=True,
    )

    ruc = serializers.CharField(
        source="empresa.ruc",
        read_only=True,
    )

    razon_social = serializers.CharField(
        source="empresa.razon_social",
        read_only=True,
    )

    nombre_comercial = serializers.CharField(
        source="empresa.nombre_comercial",
        read_only=True,
    )

    rol_nombre = serializers.CharField(
        source="get_rol_display",
        read_only=True,
    )

    sucursales = SucursalDisponibleSerializer(
        source="empresa.sucursales_activas",
        many=True,
        read_only=True,
    )

    class Meta:
        model = Membresia
        fields = (
            "id",
            "empresa_id",
            "ruc",
            "razon_social",
            "nombre_comercial",
            "rol",
            "rol_nombre",
            "estado",
            "sucursales",
        )
        read_only_fields = fields