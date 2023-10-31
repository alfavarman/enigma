from decimal import Decimal

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Order, OrderProduct, Product, ProductCategory


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["name", "description", "price", "category", "image", "thumbnail"]


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ["name"]


class OrderProductSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = OrderProduct
        fields = ["product", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(source="orderproduct_set", many=True)

    class Meta:
        model = Order
        fields = ["delivery_address", "products"]

    def create(self, validated_data):
        orders_products_data = validated_data.pop("orderproduct_set")
        order = Order.objects.create(**validated_data)

        total_price = Decimal(0.0)
        for order_data in orders_products_data:
            product = Product.objects.get(name=order_data["product"])
            quantity = order_data["quantity"]
            total_price += product.price * quantity
            OrderProduct.objects.create(order=order, **order_data)

        order.total_price = total_price
        order.save()
        return order


class ProductStatisticsInputSerializer(serializers.Serializer):
    date_from = serializers.DateField()
    date_to = serializers.DateField()
    number_of_products = serializers.IntegerField()
