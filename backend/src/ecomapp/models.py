from django.contrib.auth.models import User
from django.db import models


class ProductCategory(models.Model):
    """Product category"""
    pass


class Product(models.Model):
    """Product model"""
    pass


class Order(models.Model):
    """Order model"""
    pass


class OrderProduct(models.Model):
    """Quantity of product for a given order."""
    pass

