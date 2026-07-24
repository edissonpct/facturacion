from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from cuentas.models import Membresia
from empresas.models import Empresa, Sucursal


class EmpresasDisponiblesTests(APITestCase):
    URL = "/api/cuentas/mis-empresas/"

    def setUp(self):
        Usuario = get_user_model()

        self.usuario = Usuario.objects.create_user(
            username="ecabrera",
            email="edisson@empresa.com",
            password="ClaveSegura123!",
        )

        self.empresa = Empresa.objects.create(
            ruc="0190123456001",
            razon_social="Empresa Activa S.A.",
            nombre_comercial="Empresa Activa",
            activo=True,
        )

        self.sucursal = Sucursal.objects.create(
            empresa=self.empresa,
            codigo="001",
            nombre="Matriz",
            direccion="Cuenca",
            es_matriz=True,
            activo=True,
        )

        self.membresia = Membresia.objects.create(
            usuario=self.usuario,
            empresa=self.empresa,
            rol=Membresia.Rol.PROPIETARIO,
            estado=Membresia.Estado.ACTIVA,
        )

    def test_requiere_autenticacion(self):
        respuesta = self.client.get(self.URL)

        self.assertEqual(
            respuesta.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_lista_empresas_del_usuario(self):
        self.client.force_authenticate(self.usuario)

        respuesta = self.client.get(self.URL)

        self.assertEqual(
            respuesta.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(respuesta.data),
            1,
        )

        self.assertEqual(
            respuesta.data[0]["empresa_id"],
            self.empresa.id,
        )

        self.assertEqual(
            respuesta.data[0]["rol"],
            Membresia.Rol.PROPIETARIO,
        )

    def test_incluye_sucursales_activas(self):
        Sucursal.objects.create(
            empresa=self.empresa,
            codigo="002",
            nombre="Sucursal inactiva",
            direccion="Quito",
            activo=False,
        )

        self.client.force_authenticate(self.usuario)

        respuesta = self.client.get(self.URL)

        sucursales = respuesta.data[0]["sucursales"]

        self.assertEqual(
            len(sucursales),
            1,
        )

        self.assertEqual(
            sucursales[0]["codigo"],
            "001",
        )

    def test_no_muestra_membresias_suspendidas(self):
        self.membresia.estado = Membresia.Estado.SUSPENDIDA
        self.membresia.save(update_fields=["estado"])

        self.client.force_authenticate(self.usuario)

        respuesta = self.client.get(self.URL)

        self.assertEqual(
            respuesta.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(respuesta.data),
            0,
        )

    def test_no_muestra_empresas_inactivas(self):
        self.empresa.activo = False
        self.empresa.save(update_fields=["activo"])

        self.client.force_authenticate(self.usuario)

        respuesta = self.client.get(self.URL)

        self.assertEqual(
            respuesta.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(respuesta.data),
            0,
        )