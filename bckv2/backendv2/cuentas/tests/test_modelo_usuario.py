from django.contrib.auth import get_user_model
from django.test import TestCase


class UsuarioModeloTests(TestCase):
    def setUp(self):
        self.Usuario = get_user_model()

        self.usuario = self.Usuario.objects.create_user(
            username="ecabrera",
            email="edisson@empresa.com",
            password="ClaveSegura123!",
            first_name="Edisson",
            last_name="Cabrera",
            telefono="0999999999",
        )

    def test_modelo_usuario_configurado_correctamente(self):
        self.assertEqual(
            self.Usuario._meta.label,
            "cuentas.Usuario",
        )

    def test_creacion_usuario(self):
        self.assertEqual(
            self.usuario.username,
            "ecabrera",
        )

        self.assertEqual(
            self.usuario.email,
            "edisson@empresa.com",
        )

        self.assertEqual(
            self.usuario.telefono,
            "0999999999",
        )

    def test_contrasena_se_guarda_cifrada(self):
        self.assertNotEqual(
            self.usuario.password,
            "ClaveSegura123!",
        )

        self.assertTrue(
            self.usuario.check_password("ClaveSegura123!")
        )

    def test_usuario_activo_por_defecto(self):
        self.assertTrue(self.usuario.is_active)

    def test_usuario_normal_no_es_staff(self):
        self.assertFalse(self.usuario.is_staff)
        self.assertFalse(self.usuario.is_superuser)

    def test_representacion_textual(self):
        self.assertEqual(
            str(self.usuario),
            "ecabrera",
        )