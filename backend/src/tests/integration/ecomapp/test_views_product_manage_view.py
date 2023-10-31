import test_init
from django.contrib.auth.models import Group, User
from django.test import Client, TestCase
from django.urls import reverse

from ecomapp.models import Product


class ProductManageViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.normal_user = User.objects.create_user(username="normaluser", password="testpass")
        self.seller_user = User.objects.create_user(username="selleruser", password="testpass")
        seller_group, created = Group.objects.get_or_create(name="Seller")
        self.seller_user.groups.add(seller_group)
        self.product1 = Product.objects.create(name="Test Product 1", description="Description 1", price=10.00)

    def tearDown(self):
        self.normal_user.delete()
        self.seller_user.delete()
        self.product1.delete()

    def test_retrieve_product_without_auth(self):
        url = reverse("product-manage", args=[self.product1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product1.name)

    def test_CRUD_without_auth(self):
        url = reverse("product-manage", args=[self.product1.pk])
        create_url = reverse("product-manage-create")

        # POST
        post_data = {"name": "New Product", "description": "New Description", "price": 15.00}
        response = self.client.post(create_url, post_data)
        self.assertEqual(response.status_code, 403)

        # PUT
        update_data = {"name": "Updated Product", "description": "Updated Description", "price": 20.00}
        response = self.client.put(url, update_data)
        self.assertEqual(response.status_code, 403)

        # DELETE
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)

    def test_CRUD_with_normal_auth(self):
        self.client.login(username="normaluser", password="testpass")
        url = reverse("product-manage", args=[self.product1.pk])
        create_url = reverse("product-manage-create")

        # POST
        post_data = {"name": "New Product", "description": "New Description", "price": 15.00}
        response = self.client.post(create_url, post_data)
        self.assertEqual(response.status_code, 403)

        # PUT
        update_data = {"name": "Updated Product", "description": "Updated Description", "price": 20.00}
        response = self.client.put(url, update_data)
        self.assertEqual(response.status_code, 403)

        # DELETE
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)

    def test_CRUD_with_seller_auth(self):
        self.client.login(username="selleruser", password="testpass")
        url = reverse("product-manage", args=[self.product1.pk])
        create_url = reverse("product-manage-create")

        # POST
        post_data = {"name": "New Product", "description": "New Description", "price": 15.00}
        response = self.client.post(create_url, post_data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Product.objects.filter(name="New Product").exists())

        # PUT
        update_data = {"name": "Updated Product", "description": "Updated Description", "price": 20.00}
        response = self.client.put(url, update_data, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.product1.refresh_from_db()
        self.assertEqual(self.product1.name, "Updated Product")

        # DELETE
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Product.objects.filter(pk=self.product1.pk).exists())
