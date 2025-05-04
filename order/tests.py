from django.test import TestCase

from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from product.models import Product
from .models import Order


class OrderTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="testpass")
        self.client.force_authenticate(user=self.user)
        self.product = Product.objects.create(name="Test Product", price=10000)

    def test_create_order(self):
        data = {
            "product": self.product.id,
            "quantity": 2
        }
        response = self.client.post("/order/create/", data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Order.objects.count(), 1)
