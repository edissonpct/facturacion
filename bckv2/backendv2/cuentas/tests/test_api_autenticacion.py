from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase


class AutenticacionAPITests(APITestCase):
    LOGIN_URL = "/api/auth/jwt/create/"
    REFRESH_URL = "/api/auth/jwt/refresh/"
    VERIFY_URL = "/api/auth/jwt/verify/"
    USUARIO_ACTUAL_URL = "/api/auth/users/me/"

    def setUp(self):
        Usuario = get_user_model()

        self.password = "ClaveSegura123!"

        self.usuario = Usuario.objects.create_user(
            username="ecabrera",
            email="edisson@empresa.com",
            password=self.password,
            first_name="Edisson",
            last_name="Cabrera",
            telefono="0999999999",
        )

    def obtener_tokens(self, identificador=None):
        datos = {
            "username": identificador or self.usuario.username,
            "password": self.password,
        }

        respuesta = self.client.post(
            self.LOGIN_URL,
            datos,
            format="json",
        )

        self.assertEqual(
            respuesta.status_code,
            status.HTTP_200_OK,
        )

        self.assertIn("access", respuesta.data)
        self.assertIn("refresh", respuesta.data)

        return respuesta.data

    def autenticar_cliente(self):
        tokens = self.obtener_tokens()

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {tokens['access']}"
        )

        return tokens

    def test_login_con_username(self):
        respuesta = self.client.post(
            self.LOGIN_URL,
            {
                "username": "ecabrera",
                "password": self.password,
            },
            format="json",
        )

        self.assertEqual(
            respuesta.status_code,
            status.HTTP_200_OK,
        )

        self.assertIn("access", respuesta.data)
        self.assertIn("refresh", respuesta.data)

    def test_login_con_correo(self):
        respuesta = self.client.post(
            self.LOGIN_URL,
            {
                "username": "edisson@empresa.com",
                "password": self.password,
            },
            format="json",
        )

        self.assertEqual(
            respuesta.status_code,
            status.HTTP_200_OK,
        )

        self.assertIn("access", respuesta.data)
        self.assertIn("refresh", respuesta.data)

    def test_login_con_contrasena_incorrecta(self):
        respuesta = self.client.post(
            self.LOGIN_URL,
            {
                "username": "ecabrera",
                "password": "ContraseñaIncorrecta",
            },
            format="json",
        )

        self.assertEqual(
            respuesta.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_usuario_actual_requiere_autenticacion(self):
        respuesta = self.client.get(
            self.USUARIO_ACTUAL_URL
        )

        self.assertEqual(
            respuesta.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_consultar_usuario_actual(self):
        self.autenticar_cliente()

        respuesta = self.client.get(
            self.USUARIO_ACTUAL_URL
        )

        self.assertEqual(
            respuesta.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            respuesta.data["id"],
            self.usuario.id,
        )

        self.assertEqual(
            respuesta.data["username"],
            "ecabrera",
        )

        self.assertEqual(
            respuesta.data["email"],
            "edisson@empresa.com",
        )

        self.assertEqual(
            respuesta.data["first_name"],
            "Edisson",
        )

        self.assertEqual(
            respuesta.data["last_name"],
            "Cabrera",
        )

        self.assertEqual(
            respuesta.data["telefono"],
            "0999999999",
        )


    def test_actualizar_perfil(self):
        self.autenticar_cliente()

        respuesta = self.client.patch(
            self.USUARIO_ACTUAL_URL,
            {
                "first_name": "Edisson Andrés",
                "last_name": "Cabrera",
                "telefono": "0987654321",
            },
            format="json",
        )

        self.assertEqual(
            respuesta.status_code,
            status.HTTP_200_OK,
        )

        self.usuario.refresh_from_db()

        self.assertEqual(
            self.usuario.first_name,
            "Edisson Andrés",
        )

        self.assertEqual(
            self.usuario.telefono,
            "0987654321",
        )

    def test_no_se_puede_modificar_id(self):
        self.autenticar_cliente()

        id_original = self.usuario.id

        respuesta = self.client.patch(
            self.USUARIO_ACTUAL_URL,
            {
                "id": 999999,
            },
            format="json",
        )

        self.assertEqual(
            respuesta.status_code,
            status.HTTP_200_OK,
        )

        self.usuario.refresh_from_db()

        self.assertEqual(
            self.usuario.id,
            id_original,
        )

    def test_no_se_puede_modificar_username_desde_perfil(self):
        self.autenticar_cliente()

        respuesta = self.client.patch(
            self.USUARIO_ACTUAL_URL,
            {
                "username": "nuevo_username",
            },
            format="json",
        )

        self.assertEqual(
            respuesta.status_code,
            status.HTTP_200_OK,
        )

        self.usuario.refresh_from_db()

        self.assertEqual(
            self.usuario.username,
            "ecabrera",
        )

    def test_renovar_access_token(self):
        tokens = self.obtener_tokens()

        respuesta = self.client.post(
            self.REFRESH_URL,
            {
                "refresh": tokens["refresh"],
            },
            format="json",
        )

        self.assertEqual(
            respuesta.status_code,
            status.HTTP_200_OK,
        )

        self.assertIn("access", respuesta.data)

    def test_verificar_access_token(self):
        tokens = self.obtener_tokens()

        respuesta = self.client.post(
            self.VERIFY_URL,
            {
                "token": tokens["access"],
            },
            format="json",
        )

        self.assertEqual(
            respuesta.status_code,
            status.HTTP_200_OK,
        )