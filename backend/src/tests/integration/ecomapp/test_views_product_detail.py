import test_init
from django.test import Client, TestCase
from django.urls import reverse
from ecomapp.models import Product


class ProductDetailViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        # Create a sample product
        self.product1 = Product.objects.create(name="Test Product 1", description="Description 1", price=10.00)

    def test_retrieve_existing_product(self):
        url = reverse('product-detail', args=[self.product1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product1.name)

    def test_retrieve_nonexistent_product(self):
        url = reverse('product-detail', args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


# TODO add test with not safe method (PUT, PATCH, DELETE)