from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.http import HttpRequest

# ModelBackend --> devuelve si un usuario es válido
class UsernameOrEmailBackend(ModelBackend):

    def authenticate(
        self,
        request: HttpRequest | None,
        username: str | None = None,
        password: str | None = None,
        **kwargs: Any,
    ):
        UserModel = get_user_model()

        identificador = username or kwargs.get(UserModel.USERNAME_FIELD)

        if not identificador or not password:
            return None

        identificador = identificador.strip()

        try:
            if "@" in identificador:
                usuario = UserModel._default_manager.get(
                    email__iexact=identificador
                )
            else:
                usuario = UserModel._default_manager.get(
                    username__iexact=identificador
                )

        except UserModel.DoesNotExist:
            # Ejecuta el hash para reducir diferencias temporales entre
            # un usuario inexistente y una contraseña incorrecta.
            UserModel().set_password(password)
            return None

        if usuario.check_password(password) and self.user_can_authenticate(usuario):
            return usuario

        return None