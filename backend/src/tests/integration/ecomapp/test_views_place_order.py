import json

# import test_init
from django.contrib.auth.models import Group, User
from django.core import mail
from django.test import Client, TestCase
from django.urls import reverse
from ecomapp.models import Order, Product


class PlaceOrderViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass")
        client_group, created = Group.objects.get_or_create(name="Client")
        self.user.groups.add(client_group)
        self.product = Product.objects.create(name="Test Product", description="Description", price=10.00)

    def test_place_order(self):
        self.client.login(username="testuser", password="testpass")

        url = reverse("place-order")
        post_data = {"delivery_address": "123 Test Street", "products": [{"product": self.product.id, "quantity": 2}]}

        response = self.client.post(url, json.dumps(post_data), content_type="application/json")
        self.assertEqual(response.status_code, 201)

        order = Order.objects.last()
        self.assertEqual(order.customer, self.user)

        expected_total = float(self.product.price) * float(post_data["products"][0]["quantity"])
        self.assertEqual(order.total_price, expected_total)

        # email
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Order Confirmation")
        self.assertIn(self.user.username, mail.outbox[0].body)
        self.assertIn(str(expected_total), mail.outbox[0].body)
