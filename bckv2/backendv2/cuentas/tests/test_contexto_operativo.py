from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from cuentas.models import Membresia
from empresas.models import Empresa, Sucursal


class ContextoOperativoTests(APITestCase):
    URL = "/api/cuentas/contexto-operativo/"

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
            activo=True,
        )

        self.membresia = Membresia.objects.create(
            usuario=self.usuario,
            empresa=self.empresa,
            rol=Membresia.Rol.PROPIETARIO,
            estado=Membresia.Estado.ACTIVA,
        )

        self.client.force_authenticate(self.usuario)

    def test_requiere_sucursal(self):
        respuesta = self.client.get(
            self.URL,
            HTTP_X_EMPRESA_ID=str(self.empresa.id),
        )

        self.assertEqual(
            respuesta.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_rechaza_identificador_de_sucursal_invalido(self):
        respuesta = self.client.get(
            self.URL,
            HTTP_X_EMPRESA_ID=str(self.empresa.id),
            HTTP_X_SUCURSAL_ID="abc",
        )

        self.assertEqual(
            respuesta.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_rechaza_sucursal_de_otra_empresa(self):
        otra_empresa = Empresa.objects.create(
            ruc="1790123456001",
            razon_social="Otra Empresa S.A.",
        )

        otra_sucursal = Sucursal.objects.create(
            empresa=otra_empresa,
            codigo="001",
            nombre="Otra Matriz",
            direccion="Quito",
            es_matriz=True,
        )

        respuesta = self.client.get(
            self.URL,
            HTTP_X_EMPRESA_ID=str(self.empresa.id),
            HTTP_X_SUCURSAL_ID=str(otra_sucursal.id),
        )

        self.assertEqual(
            respuesta.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_rechaza_sucursal_inactiva(self):
        self.sucursal.activo = False
        self.sucursal.save(update_fields=["activo"])

        respuesta = self.client.get(
            self.URL,
            HTTP_X_EMPRESA_ID=str(self.empresa.id),
            HTTP_X_SUCURSAL_ID=str(self.sucursal.id),
        )

        self.assertEqual(
            respuesta.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_devuelve_contexto_operativo(self):
        respuesta = self.client.get(
            self.URL,
            HTTP_X_EMPRESA_ID=str(self.empresa.id),
            HTTP_X_SUCURSAL_ID=str(self.sucursal.id),
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
            respuesta.data["sucursal"]["id"],
            self.sucursal.id,
        )

        self.assertEqual(
            respuesta.data["membresia"]["rol"],
            Membresia.Rol.PROPIETARIO,
        )