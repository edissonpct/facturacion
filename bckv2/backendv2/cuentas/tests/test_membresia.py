from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import TestCase

from cuentas.models import Membresia
from empresas.models import Empresa, Sucursal


class MembresiaModeloTests(TestCase):
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
            nombre_comercial="Empresa de Prueba",
        )

        self.sucursal_matriz = Sucursal.objects.create(
            empresa=self.empresa,
            codigo="001",
            nombre="Matriz",
            direccion="Cuenca, Ecuador",
            es_matriz=True,
        )

        self.membresia = Membresia.objects.create(
            usuario=self.usuario,
            empresa=self.empresa,
            rol=Membresia.Rol.PROPIETARIO,
            estado=Membresia.Estado.ACTIVA,
        )

    def test_crear_membresia(self):
        self.assertEqual(
            self.membresia.usuario,
            self.usuario,
        )

        self.assertEqual(
            self.membresia.empresa,
            self.empresa,
        )

        self.assertEqual(
            self.membresia.rol,
            Membresia.Rol.PROPIETARIO,
        )

        self.assertEqual(
            self.membresia.estado,
            Membresia.Estado.ACTIVA,
        )

    def test_valores_predeterminados(self):
        Usuario = get_user_model()

        otro_usuario = Usuario.objects.create_user(
            username="empleado",
            email="empleado@empresa.com",
            password="ClaveSegura123!",
        )

        membresia = Membresia.objects.create(
            usuario=otro_usuario,
            empresa=self.empresa,
        )

        self.assertEqual(
            membresia.rol,
            Membresia.Rol.EMPLEADO,
        )

        self.assertEqual(
            membresia.estado,
            Membresia.Estado.PENDIENTE,
        )

    def test_usuario_no_puede_repetirse_en_misma_empresa(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Membresia.objects.create(
                    usuario=self.usuario,
                    empresa=self.empresa,
                    rol=Membresia.Rol.ADMINISTRADOR,
                    estado=Membresia.Estado.ACTIVA,
                )

    def test_usuario_puede_pertenecer_a_varias_empresas(self):
        otra_empresa = Empresa.objects.create(
            ruc="1790123456001",
            razon_social="Otra Empresa S.A.",
        )

        otra_membresia = Membresia.objects.create(
            usuario=self.usuario,
            empresa=otra_empresa,
            rol=Membresia.Rol.CONTADOR_EXTERNO,
            estado=Membresia.Estado.ACTIVA,
        )

        self.assertEqual(
            self.usuario.membresias.count(),
            2,
        )

        self.assertEqual(
            otra_membresia.empresa,
            otra_empresa,
        )

    def test_varios_usuarios_pueden_pertenecer_a_misma_empresa(self):
        Usuario = get_user_model()

        otro_usuario = Usuario.objects.create_user(
            username="contador",
            email="contador@empresa.com",
            password="ClaveSegura123!",
        )

        Membresia.objects.create(
            usuario=otro_usuario,
            empresa=self.empresa,
            rol=Membresia.Rol.CONTADOR_EXTERNO,
            estado=Membresia.Estado.ACTIVA,
        )

        self.assertEqual(
            self.empresa.membresias.count(),
            2,
        )

    def test_relacion_inversa_desde_usuario(self):
        self.assertEqual(
            self.usuario.membresias.count(),
            1,
        )

        self.assertEqual(
            self.usuario.membresias.first(),
            self.membresia,
        )

    def test_relacion_inversa_desde_empresa(self):
        self.assertEqual(
            self.empresa.membresias.count(),
            1,
        )

        self.assertEqual(
            self.empresa.membresias.first(),
            self.membresia,
        )

    def test_membresia_da_acceso_a_sucursales_de_empresa(self):
        segunda_sucursal = Sucursal.objects.create(
            empresa=self.empresa,
            codigo="002",
            nombre="Sucursal Norte",
            direccion="Cuenca, Ecuador",
            es_matriz=False,
        )

        sucursales = self.membresia.empresa.sucursales.all()

        self.assertEqual(
            sucursales.count(),
            2,
        )

        self.assertIn(
            self.sucursal_matriz,
            sucursales,
        )

        self.assertIn(
            segunda_sucursal,
            sucursales,
        )

    def test_eliminar_usuario_elimina_sus_membresias(self):
        usuario_id = self.usuario.id

        self.usuario.delete()

        self.assertFalse(
            Membresia.objects.filter(
                usuario_id=usuario_id,
            ).exists()
        )

    def test_eliminar_empresa_elimina_sus_membresias(self):
        empresa_id = self.empresa.id

        self.empresa.delete()

        self.assertFalse(
            Membresia.objects.filter(
                empresa_id=empresa_id,
            ).exists()
        )

    def test_representacion_textual(self):
        self.assertEqual(
            str(self.membresia),
            (
                "ecabrera - "
                "Empresa de Prueba S.A. - "
                "Propietario"
            ),
        )

    def test_etiquetas_de_roles(self):
        self.assertEqual(
            Membresia.Rol.PROPIETARIO.label,
            "Propietario",
        )

        self.assertEqual(
            Membresia.Rol.CONTADOR_EXTERNO.label,
            "Contador externo",
        )

    def test_etiquetas_de_estados(self):
        self.assertEqual(
            Membresia.Estado.ACTIVA.label,
            "Activa",
        )

        self.assertEqual(
            Membresia.Estado.SUSPENDIDA.label,
            "Suspendida",
        )