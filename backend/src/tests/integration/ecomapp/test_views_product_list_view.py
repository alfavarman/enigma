import test_init
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status

from ecomapp.models import Product, ProductCategory
from ecomapp.serializers import ProductSerializer


class ProductListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url_list = "product-list"

        category = ProductCategory.objects.create(name="Electronics")
        for i in range(15):
            Product.objects.create(
                name=f"Product {i}", description=f"Description for product {i}", price=i + 10.50, category=category
            )

    def test_list_products_with_pagination(self):
        url = reverse(self.url_list)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 10)  # pagination

        products = Product.objects.all()[:10]
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(response.data["results"], serializer.data)

    def test_search_products(self):
        url = reverse(self.url_list)
        response = self.client.get(url, {"search": "Product 11"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][1]["name"], "Product 11")

    def test_filter_by_category_name(self):
        url = reverse(self.url_list)
        response = self.client.get(url, {"category__name": "Electronics"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data["results"]) > 0)
        self.assertEqual(response.data["results"][0]["category"], 1)

    def test_ordering_by_name(self):
        url = reverse(self.url_list)
        response = self.client.get(url, {"ordering": "name"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product_names = [product["name"] for product in response.data["results"]]
        self.assertEqual(product_names, sorted(product_names))

    def test_ordering_by_price_desc(self):
        url = reverse(self.url_list)
        response = self.client.get(url, {"ordering": "-price"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product_prices = [product["price"] for product in response.data["results"]]
        self.assertEqual(product_prices, sorted(product_prices, reverse=True))
