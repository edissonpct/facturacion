from djoser.serializers import (
    UserCreatePasswordRetypeSerializer,
    UserSerializer,
)
from rest_framework import serializers

from .models import Usuario



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