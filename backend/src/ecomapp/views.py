from rest_framework import generics, filters, pagination
from .models import Product
from .serializers import ProductSerializer


class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    pagination_class = pagination.PageNumberPagination
    pagination_class.page_size = 10

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "category__name", "description",  "price"]
    ordering_fields = ["name", "category__name", "price"]


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

