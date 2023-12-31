from django.core.mail import send_mail
from django.db.models import Sum
from rest_framework import filters, generics, pagination, permissions
from rest_framework.response import Response

from .models import Order, OrderProduct, Product
from .serializers import OrderSerializer, ProductSerializer, ProductStatisticsInputSerializer


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


class PlaceOrderView(generics.CreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        return [permissions.IsAuthenticated(), IsClient()]

    def perform_create(self, serializer):
        order = serializer.save(customer=self.request.user)
        self.send_order_confirmation_email(order)

    @staticmethod
    def send_order_confirmation_email(order):
        send_mail(
            "Order Confirmation",
            f"Hello {order.customer.username}, your order has been placed successfully. "
            f"The total price is {order.total_price} and the payment due date is {order.payment_due_date}.",
            "from@example.com",
            [order.customer.email],
            fail_silently=False,
        )


class ProductStatisticsView(generics.RetrieveAPIView):
    def get_permissions(self):
        return [permissions.IsAuthenticated(), IsSeller()]

    def get(self, request, *args, **kwargs):
        serializer = ProductStatisticsInputSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        date_from = serializer.validated_data["date_from"]
        date_to = serializer.validated_data["date_to"]
        number_of_products = serializer.validated_data["number_of_products"]

        order_products = OrderProduct.objects.filter(order__order_date__range=(date_from, date_to))

        product_quantities = (
            order_products.values("product__name")
            .annotate(total_quantity=Sum("quantity"))
            .order_by("-total_quantity")[:number_of_products]
        )

        return Response(product_quantities)
