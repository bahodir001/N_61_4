from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User


class AuthTestCase(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpass123"
        }
        self.client.post(self.register_url, self.user_data)

    def test_register_user(self):
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "newpass123"
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_user(self):
        response = self.client.post(self.login_url, {
            "username": self.user_data["username"],
            "password": self.user_data["password"]
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

