from django.urls import path

from .views import ContextoEmpresaView, EmpresasDisponiblesView


app_name = "cuentas"

urlpatterns = [
    path(
        "mis-empresas/",
        EmpresasDisponiblesView.as_view(),
        name="empresas-disponibles",
    ),
    path(
        "contexto/",
        ContextoEmpresaView.as_view(),
        name="contexto-empresa",
    ),
]