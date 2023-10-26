from django.contrib.auth.models import User
from django.db import models


class ProductCategory(models.Model):
    """Product category"""
    name = models.CharField(max_length=120, verbose_name="Name", unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    """Product."""
    name = models.CharField(max_length=120, verbose_name="Name")
    description = models.TextField(verbose_name="Description")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True, verbose_name="Category")
    image = models.ImageField(upload_to='products/', verbose_name="Image")
    thumbnail = models.ImageField(upload_to='products/thumbnails/', verbose_name="Thumbnail Image")

    def __str__(self):
        return self.name


class Order(models.Model):
    """Order model"""
    pass


class OrderProduct(models.Model):
    """Quantity of product for a given order."""
    pass
