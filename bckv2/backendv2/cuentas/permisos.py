from rest_framework.permissions import BasePermission

from empresas.models import Sucursal

from .models import Membresia


class EmpresaActiva(BasePermission):
    """
    Valida la empresa seleccionada y la membresía activa del usuario.

    Agrega:
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


class SucursalActiva(BasePermission):
    """
    Valida que la sucursal seleccionada esté activa y pertenezca
    a la empresa previamente validada por EmpresaActiva.

    Agrega:
    request.sucursal
    """

    message = "La sucursal seleccionada no es válida."

    def has_permission(self, request, view):
        empresa = getattr(request, "empresa", None)

        if empresa is None:
            self.message = "Primero debe seleccionar una empresa válida."
            return False

        sucursal_id = request.headers.get("X-Sucursal-ID")

        if not sucursal_id:
            self.message = (
                "Debe seleccionar una sucursal mediante "
                "el encabezado X-Sucursal-ID."
            )
            return False

        try:
            sucursal_id = int(sucursal_id)
        except (TypeError, ValueError):
            self.message = "El identificador de sucursal no es válido."
            return False

        sucursal = (
            Sucursal.objects
            .filter(
                id=sucursal_id,
                empresa=empresa,
                activo=True,
            )
            .first()
        )

        if sucursal is None:
            self.message = (
                "La sucursal no existe, está inactiva o no pertenece "
                "a la empresa seleccionada."
            )
            return False

        request.sucursal = sucursal

        return True