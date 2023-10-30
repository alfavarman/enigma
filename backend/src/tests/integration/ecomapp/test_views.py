# Import the test initialization module
# import test_init


from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status

from ecomapp.models import Product, ProductCategory
from ecomapp.serializers import ProductSerializer


class ProductListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("product-list")

    def test_list_products(self):
        # Setting up a category for use in product creation.
        category = ProductCategory.objects.create(name="Electronics")

        # Creating 15 products to test pagination.
        for i in range(15):
            Product.objects.create(
                name=f"Product {i}",
                description=f"Description for product {i}",
                price=i + 10.50,
                category=category
            )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)  # pagination

        products = Product.objects.all()[:10]
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(response.data['results'], serializer.data)

    # def test_search_products(self):
    #     response = self.client.get(self.url, {'search': 'Product 1'})
    #
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data['results']), 1)
    #     self.assertEqual(response.data['results'][0]['name'], 'Product 1')
    #
    # def test_retrieve_non_exist_product(self):
    #     response = self.client.get(self.url, 'product-detail', args=[1000])})
    #     url = reverse('product-detail', args=[1000])
    #     response = self.client.get(url)
    #
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    #     self.assertEqual(response.data, {"detail": "Not found."})
