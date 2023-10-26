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
    customer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Customer")
    delivery_address = models.TextField(verbose_name="Delivery Address")
    order_date = models.DateTimeField(auto_now_add=True, verbose_name="Order Date")
    payment_due_date = models.DateTimeField(verbose_name="Payment Due Date")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Price")

    # This will be a many-to-many relationship to handle products and their quantities
    products = models.ManyToManyField(Product, through='OrderProduct', verbose_name="Products")

    def __str__(self):
        return f"Order {self.id} by {self.customer.username}"


class OrderProduct(models.Model):
    """Quantity of product for a given order."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Order")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Product")
    quantity = models.PositiveIntegerField(verbose_name="Quantity")

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"



### TODO : COMMENT: 1) django inherit the id fields from the parent class,
# however for some cases like products where ids will be generated, added, removed etc we would use UUID insted
# of autoincrement primary key. As for simplicity of project SQL lite is used which stores UUID as TEXT todo is marked.
