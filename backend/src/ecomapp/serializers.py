from rest_framework import serializers
from .models import Product, ProductCategory, OrderProduct, Order


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["name", "description", "price", "category", "image", "thumbnail"]


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ["name"]


class OrderProductSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(source="product", queryset=Product.objects.all())
    quantity = serializers.IntegerField()

    class Meta:
        model = OrderProduct
        fields = ["product_id", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True)

    class Meta:
        model = Order
        fields = ["customer", "delivery_address", "products"]

    def create(self, validated_data):
        products_data = validated_data.pop("products")
        order = Order.objects.create(**validated_data)

        for product_data in products_data:
            OrderProduct.objects.create(order=order, **product_data)

        return order


class ProductStatisticsInputSerializer(serializers.Serializer):
    date_from = serializers.DateField()
    date_to = serializers.DateField()
    number_of_products = serializers.IntegerField()
