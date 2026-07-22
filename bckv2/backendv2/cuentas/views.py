from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .permisos import EmpresaActiva
from django.db.models import Prefetch
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from empresas.models import Sucursal

from .models import Membresia
from .serializers import EmpresaDisponibleSerializer


class ContextoEmpresaView(APIView):
    permission_classes = [
        IsAuthenticated,
        EmpresaActiva,
    ]

    def get(self, request):
        sucursales = list(
            request.empresa.sucursales
            .filter(activo=True)
            .values(
                "id",
                "codigo",
                "nombre",
                "es_matriz",
            )
        )

        return Response(
            {
                "usuario": {
                    "id": request.user.id,
                    "username": request.user.username,
                    "email": request.user.email,
                },
                "membresia": {
                    "id": request.membresia.id,
                    "rol": request.membresia.rol,
                    "rol_nombre": request.membresia.get_rol_display(),
                    "estado": request.membresia.estado,
                },
                "empresa": {
                    "id": request.empresa.id,
                    "ruc": request.empresa.ruc,
                    "razon_social": request.empresa.razon_social,
                    "nombre_comercial": request.empresa.nombre_comercial,
                },
                "sucursales": sucursales,
            }
        )


class EmpresasDisponiblesView(ListAPIView):
    """
    Lista las empresas activas en las que el usuario
    autenticado tiene una membresía activa.
    """

    serializer_class = EmpresaDisponibleSerializer

    permission_classes = [
        IsAuthenticated,
    ]

    pagination_class = None

    def get_queryset(self):
        sucursales_activas = (
            Sucursal.objects
            .filter(activo=True)
            .order_by("codigo")
        )

        return (
            Membresia.objects
            .select_related("empresa")
            .prefetch_related(
                Prefetch(
                    "empresa__sucursales",
                    queryset=sucursales_activas,
                    to_attr="sucursales_activas",
                )
            )
            .filter(
                usuario=self.request.user,
                estado=Membresia.Estado.ACTIVA,
                empresa__activo=True,
            )
            .order_by(
                "empresa__razon_social",
            )
        )