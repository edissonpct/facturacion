from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase

from empresas.models import Empresa, Sucursal


class EmpresaModeloTests(TestCase):
    def setUp(self):
        self.empresa = Empresa.objects.create(
            ruc="0190123456001",
            razon_social="Empresa de Prueba S.A.",
            nombre_comercial="Empresa de Prueba",
            email="administracion@empresa.com",
            telefono="072888888",
        )

    def test_crear_empresa(self):
        self.assertEqual(
            self.empresa.razon_social,
            "Empresa de Prueba S.A.",
        )
        self.assertEqual(
            self.empresa.ruc,
            "0190123456001",
        )
        self.assertTrue(self.empresa.activo)

    def test_representacion_textual(self):
        self.assertEqual(
            str(self.empresa),
            "Empresa de Prueba S.A. - 0190123456001",
        )

    def test_ruc_debe_tener_trece_digitos(self):
        empresa = Empresa(
            ruc="123456",
            razon_social="Empresa Inválida",
        )

        with self.assertRaises(ValidationError):
            empresa.full_clean()

    def test_ruc_solo_admite_numeros(self):
        empresa = Empresa(
            ruc="0190123456ABC",
            razon_social="Empresa Inválida",
        )

        with self.assertRaises(ValidationError):
            empresa.full_clean()

    def test_ruc_no_puede_repetirse(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Empresa.objects.create(
                    ruc="0190123456001",
                    razon_social="Empresa Duplicada",
                )


class SucursalModeloTests(TestCase):
    def setUp(self):
        self.empresa = Empresa.objects.create(
            ruc="0190123456001",
            razon_social="Empresa de Prueba S.A.",
        )

        self.sucursal = Sucursal.objects.create(
            empresa=self.empresa,
            codigo="001",
            nombre="Matriz",
            direccion="Cuenca, Ecuador",
            es_matriz=True,
        )

    def test_crear_sucursal(self):
        self.assertEqual(self.sucursal.codigo, "001")
        self.assertEqual(self.sucursal.empresa, self.empresa)
        self.assertTrue(self.sucursal.es_matriz)
        self.assertTrue(self.sucursal.activo)

    def test_relacion_inversa_empresa_sucursales(self):
        self.assertEqual(
            self.empresa.sucursales.count(),
            1,
        )

        self.assertEqual(
            self.empresa.sucursales.first(),
            self.sucursal,
        )

    def test_codigo_debe_tener_tres_digitos(self):
        sucursal = Sucursal(
            empresa=self.empresa,
            codigo="1",
            nombre="Sucursal inválida",
            direccion="Cuenca",
        )

        with self.assertRaises(ValidationError):
            sucursal.full_clean()

    def test_codigo_no_puede_repetirse_en_misma_empresa(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Sucursal.objects.create(
                    empresa=self.empresa,
                    codigo="001",
                    nombre="Sucursal duplicada",
                    direccion="Quito",
                )

    def test_codigo_puede_repetirse_en_empresas_diferentes(self):
        otra_empresa = Empresa.objects.create(
            ruc="1790123456001",
            razon_social="Otra Empresa S.A.",
        )

        otra_sucursal = Sucursal.objects.create(
            empresa=otra_empresa,
            codigo="001",
            nombre="Matriz",
            direccion="Quito, Ecuador",
            es_matriz=True,
        )

        self.assertEqual(otra_sucursal.codigo, "001")
        self.assertNotEqual(
            otra_sucursal.empresa,
            self.sucursal.empresa,
        )

    def test_empresa_no_puede_tener_dos_matrices(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Sucursal.objects.create(
                    empresa=self.empresa,
                    codigo="002",
                    nombre="Segunda matriz",
                    direccion="Quito, Ecuador",
                    es_matriz=True,
                )

    def test_empresa_puede_tener_varias_sucursales_no_matriz(self):
        segunda_sucursal = Sucursal.objects.create(
            empresa=self.empresa,
            codigo="002",
            nombre="Sucursal Norte",
            direccion="Cuenca, Ecuador",
            es_matriz=False,
        )

        tercera_sucursal = Sucursal.objects.create(
            empresa=self.empresa,
            codigo="003",
            nombre="Sucursal Sur",
            direccion="Cuenca, Ecuador",
            es_matriz=False,
        )

        self.assertEqual(
            self.empresa.sucursales.count(),
            3,
        )
        self.assertFalse(segunda_sucursal.es_matriz)
        self.assertFalse(tercera_sucursal.es_matriz)

    def test_eliminar_empresa_elimina_sucursales(self):
        empresa_id = self.empresa.id

        self.empresa.delete()

        self.assertFalse(
            Sucursal.objects.filter(
                empresa_id=empresa_id
            ).exists()
        )

    def test_representacion_textual(self):
        self.assertEqual(
            str(self.sucursal),
            "Empresa de Prueba S.A. - 001 - Matriz",
        )