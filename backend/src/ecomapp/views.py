from datetime import datetime, timedelta

from django.core.mail import send_mail
from django.db.models import Sum
from rest_framework import generics, filters, pagination, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, Order, OrderProduct
from .serializers import ProductSerializer, OrderSerializer, ProductStatisticsInputSerializer


class IsSeller(permissions.BasePermission):
    """
    Verify that the user has seller-group permission
    """

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Seller").exists()


class IsClient(permissions.BasePermission):
    """
    Verify that the user has client permission
    """

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Client").exists()


class ProductListView(generics.ListAPIView):
    """
    views for listing and creating products - no authorization required
    methods allowed: GET
    """

    queryset = Product.objects.all().order_by("id")
    serializer_class = ProductSerializer

    pagination_class = pagination.PageNumberPagination
    pagination_class.page_size = 10

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "category__name", "description", "price"]
    ordering_fields = ["name", "category__name", "price"]


class ProductDetailView(generics.RetrieveAPIView):
    """
    views for listing and creating products - no authorization required
    methods allowed: GET
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductManageView(generics.RetrieveUpdateDestroyAPIView, generics.CreateAPIView):
    """Manage a product,
    GET - no auth
    POST - auth, seller group permissions only
    PUT - auth, seller group permissions only
    DELETE - auth, seller group permissions only
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsSeller()]


class PlaceOrderView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated(), IsClient()]

    def perform_create(self, serializer):
        order = serializer.save(customer=self.request.user)

        # Calculate total price of the products in the order
        total_price = sum(
            [order_product.product.price * order_product.quantity for order_product in order.orderproduct_set.all()]
        )
        order.total_price = total_price

        # Calculate the payment due date
        order.payment_due_date = datetime.now() + timedelta(days=5)
        order.save()

        # Send a confirmation email
        send_mail(
            "Order Confirmation",
            f"Hello {order.customer.username}, your order has been placed successfully. "
            f"The total price is {total_price} and the payment due date is {order.payment_due_date}.",
            "from@example.com",
            [order.customer.email],
            fail_silently=False,
        )


class ProductStatisticsView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsSeller()]

    def get(self, request, *args, **kwargs):
        serializer = ProductStatisticsInputSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        date_from = serializer.validated_data["date_from"]
        date_to = serializer.validated_data["date_to"]
        number_of_products = serializer.validated_data["number_of_products"]

        # Filtering the OrderProduct based on the date range of Orders.
        order_products = OrderProduct.objects.filter(order__order_date__range=(date_from, date_to))

        # Aggregating product quantities
        product_quantities = (
            order_products.values("product__name")
            .annotate(total_quantity=Sum("quantity"))
            .order_by("-total_quantity")[:number_of_products]
        )

        return Response(product_quantities)
