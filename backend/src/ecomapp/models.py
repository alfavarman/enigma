from pathlib import Path

from PIL import Image as Img
from django.conf import settings
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
    image = models.ImageField(upload_to="products/", verbose_name="Image", null=True, blank=True)
    thumbnail = models.ImageField(
        upload_to="products/thumbnails/", verbose_name="Thumbnail Image", blank=True, null=True
    )

    class Meta:
        permissions = [
            ("can_view_product_statistics", "Can view product statistics"),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.image:
            self.thumbnail = None  # This will not delete the file from the storage.
        else:
            thb_rel_path = Product.generate_thumbnail(self.image.path)
            self.thumbnail = thb_rel_path

        super().save(*args, **kwargs)

    @staticmethod
    def generate_thumbnail(image_path):
        size = 200, 200
        im = Img.open(image_path)
        im.thumbnail(size, Img.ANTIALIAS)
        name = Path(image_path)
        thb_path = Path(settings.MEDIA_ROOT) / "products/thumbnails/" / f"thumb_{name.stem}.png"
        im.save(thb_path, "PNG")
        return thb_path.relative_to(Path(settings.MEDIA_ROOT))


class Order(models.Model):
    """Order model"""

    customer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Customer")
    delivery_address = models.TextField(verbose_name="Delivery Address")
    order_date = models.DateTimeField(auto_now_add=True, verbose_name="Order Date")
    payment_due_date = models.DateTimeField(verbose_name="Payment Due Date")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Price")

    # This will be a many-to-many relationship to handle products and their quantities
    products = models.ManyToManyField(Product, through="OrderProduct", verbose_name="Products")

    def __str__(self):
        return f"Order {self.id} by {self.customer.username}"


class OrderProduct(models.Model):
    """Quantity of product for a given order."""

    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Order")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Product")
    quantity = models.PositiveIntegerField(verbose_name="Quantity")

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


# TODO models to separate modules (model folder + init + model_name.py)

### TODO : COMMENT: 1) django inherit the id fields from the parent class,
# however for some cases like products where ids will be generated, added, removed etc we would use UUID insted
# of autoincrement primary key. As for simplicity of project SQL lite is used which stores UUID as TEXT todo is marked.
