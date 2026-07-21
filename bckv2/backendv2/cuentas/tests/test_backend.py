from django.contrib.auth import authenticate, get_user_model
from django.test import TestCase


class UsernameOrEmailBackendTests(TestCase):
    def setUp(self):
        Usuario = get_user_model()

        self.password = "ClaveSegura123!"

        self.usuario = Usuario.objects.create_user(
            username="ecabrera",
            email="edisson@empresa.com",
            password=self.password,
        )

    def test_autenticar_con_username(self):
        usuario_autenticado = authenticate(
            username="ecabrera",
            password=self.password,
        )

        self.assertIsNotNone(usuario_autenticado)

        self.assertEqual(
            usuario_autenticado.pk,
            self.usuario.pk,
        )

    def test_autenticar_con_correo(self):
        usuario_autenticado = authenticate(
            username="edisson@empresa.com",
            password=self.password,
        )

        self.assertIsNotNone(usuario_autenticado)

        self.assertEqual(
            usuario_autenticado.pk,
            self.usuario.pk,
        )

    def test_correo_no_distingue_mayusculas(self):
        usuario_autenticado = authenticate(
            username="EDISSON@EMPRESA.COM",
            password=self.password,
        )

        self.assertIsNotNone(usuario_autenticado)

        self.assertEqual(
            usuario_autenticado.pk,
            self.usuario.pk,
        )

    def test_username_no_distingue_mayusculas(self):
        usuario_autenticado = authenticate(
            username="ECABRERA",
            password=self.password,
        )

        self.assertIsNotNone(usuario_autenticado)

        self.assertEqual(
            usuario_autenticado.pk,
            self.usuario.pk,
        )

    def test_contrasena_incorrecta(self):
        usuario_autenticado = authenticate(
            username="ecabrera",
            password="ContraseñaIncorrecta",
        )

        self.assertIsNone(usuario_autenticado)

    def test_usuario_inexistente(self):
        usuario_autenticado = authenticate(
            username="usuario_inexistente",
            password=self.password,
        )

        self.assertIsNone(usuario_autenticado)

    def test_usuario_inactivo_no_puede_autenticarse(self):
        self.usuario.is_active = False
        self.usuario.save(update_fields=["is_active"])

        usuario_autenticado = authenticate(
            username="ecabrera",
            password=self.password,
        )

        self.assertIsNone(usuario_autenticado)