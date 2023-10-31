import datetime
from django.utils import timezone

import test_init
from django.contrib.auth.models import User, Group
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from ecomapp.models import Product, Order, OrderProduct


class ProductStatisticsViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.seller = User.objects.create_user(username='seller1', password='pass1234')
        seller_group, created = Group.objects.get_or_create(name="Seller")
        self.seller.groups.add(seller_group)
        self.seller.save()

        self.test_date = timezone.now().astimezone(datetime.timezone.utc)

        self.product_1 = Product.objects.create(name='Product1', price=10.00)
        self.product_2 = Product.objects.create(name='Product2', price=20.00)

        self.order = Order.objects.create(customer=self.seller, order_date=self.test_date)
        OrderProduct.objects.create(order=self.order, product=self.product_1, quantity=5)
        OrderProduct.objects.create(order=self.order, product=self.product_2, quantity=10)

        self.client.force_authenticate(user=self.seller)

    def tearDown(self):
        self.seller.delete()
        self.product_1.delete()
        self.product_2.delete()
        self.order.delete()
        OrderProduct.objects.all().delete()

    def test_get_product_statistics_success(self):
        url = reverse('product-statistics')

        params = {
            "date_from": self.test_date.strftime('%Y-%m-%d'),
            "date_to": (self.test_date + datetime.timedelta(days=1)).strftime('%Y-%m-%d'),
            "number_of_products": 2
        }

        response = self.client.get(url, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = [
            {"product__name": "Product2", "total_quantity": 10},
            {"product__name": "Product1", "total_quantity": 5}
        ]
        self.assertEqual(list(response.data), expected_data)

    def test_get_product_statistics_missing_date(self):
        url = reverse('product-statistics')

        params = {
            "date_from": self.test_date.strftime('%Y-%m-%d'),
            "number_of_products": 2
        }

        response = self.client.get(url, params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

