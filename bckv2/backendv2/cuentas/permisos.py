from rest_framework.permissions import BasePermission

from .models import Membresia


class EmpresaActiva(BasePermission):
    """
    Verifica que la petición incluya una empresa válida y que
    el usuario tenga una membresía activa en ella.

    Si la validación es correcta, agrega a la petición:

    request.empresa
    request.membresia
    """

    message = "No tiene acceso a la empresa seleccionada."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            self.message = "Debe iniciar sesión."
            return False

        empresa_id = request.headers.get("X-Empresa-ID")

        if not empresa_id:
            self.message = (
                "Debe seleccionar una empresa mediante "
                "el encabezado X-Empresa-ID."
            )
            return False

        try:
            empresa_id = int(empresa_id)
        except (TypeError, ValueError):
            self.message = "El identificador de empresa no es válido."
            return False

        membresia = (
            Membresia.objects
            .select_related("empresa")
            .filter(
                usuario=request.user,
                empresa_id=empresa_id,
                estado=Membresia.Estado.ACTIVA,
                empresa__activo=True,
            )
            .first()
        )

        if membresia is None:
            self.message = (
                "No tiene una membresía activa en la empresa seleccionada."
            )
            return False

        request.empresa = membresia.empresa
        request.membresia = membresia

        return True