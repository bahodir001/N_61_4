from django.test import TestCase

from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Product
from .models import Like


class LikeTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="testpass")
        self.client.force_authenticate(user=self.user)
        self.product = Product.objects.create(name="Product 1", price=5000)

    def test_like_product(self):
        response = self.client.post(f"/product/{self.product.id}/like/")
        self.assertEqual(response.status_code, 201)

    def test_get_likes(self):
        self.client.post(f"/product/{self.product.id}/like/")
        response = self.client.get("/product/likes/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data) > 0)
