from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from cuentas.models import Membresia
from empresas.models import Empresa, Sucursal


class ContextoEmpresaTests(TestCase):
    URL = "/api/cuentas/contexto/"

    def setUp(self):
        Usuario = get_user_model()

        self.usuario = Usuario.objects.create_user(
            username="ecabrera",
            email="edisson@empresa.com",
            password="ClaveSegura123!",
        )

        self.empresa = Empresa.objects.create(
            ruc="0190123456001",
            razon_social="Empresa de Prueba S.A.",
        )

        self.sucursal = Sucursal.objects.create(
            empresa=self.empresa,
            codigo="001",
            nombre="Matriz",
            direccion="Cuenca",
            es_matriz=True,
        )

        self.membresia = Membresia.objects.create(
            usuario=self.usuario,
            empresa=self.empresa,
            rol=Membresia.Rol.PROPIETARIO,
            estado=Membresia.Estado.ACTIVA,
        )

        self.client = APIClient()
        self.client.force_authenticate(self.usuario)

    def test_requiere_empresa_en_encabezado(self):
        respuesta = self.client.get(self.URL)

        self.assertEqual(
            respuesta.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_rechaza_identificador_invalido(self):
        respuesta = self.client.get(
            self.URL,
            HTTP_X_EMPRESA_ID="abc",
        )

        self.assertEqual(
            respuesta.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_rechaza_empresa_sin_membresia(self):
        otra_empresa = Empresa.objects.create(
            ruc="1790123456001",
            razon_social="Otra Empresa S.A.",
        )

        respuesta = self.client.get(
            self.URL,
            HTTP_X_EMPRESA_ID=str(otra_empresa.id),
        )

        self.assertEqual(
            respuesta.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_rechaza_membresia_no_activa(self):
        self.membresia.estado = Membresia.Estado.SUSPENDIDA
        self.membresia.save(update_fields=["estado"])

        respuesta = self.client.get(
            self.URL,
            HTTP_X_EMPRESA_ID=str(self.empresa.id),
        )

        self.assertEqual(
            respuesta.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_devuelve_contexto_de_empresa(self):
        respuesta = self.client.get(
            self.URL,
            HTTP_X_EMPRESA_ID=str(self.empresa.id),
        )

        self.assertEqual(
            respuesta.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            respuesta.data["empresa"]["id"],
            self.empresa.id,
        )

        self.assertEqual(
            respuesta.data["membresia"]["rol"],
            Membresia.Rol.PROPIETARIO,
        )

        self.assertEqual(
            len(respuesta.data["sucursales"]),
            1,
        )