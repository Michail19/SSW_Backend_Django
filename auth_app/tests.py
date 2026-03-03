from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass",
            level="OWNER"
        )

    def test_login_success(self):
        response = self.client.post("/auth/login/", {
            "username": "testuser",
            "password": "testpass"
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.data)

    def test_login_invalid(self):
        response = self.client.post("/auth/login/", {
            "username": "testuser",
            "password": "wrong"
        })

        self.assertEqual(response.status_code, 401)

    def test_verify_owner_access(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get("/auth/verify/")
        self.assertEqual(response.status_code, 200)
