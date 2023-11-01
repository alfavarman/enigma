from django.contrib import admin
from django.urls import include, path
from ecomapp.views import PlaceOrderView, ProductDetailView, ProductListView, ProductManageView, ProductStatisticsView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("django.contrib.auth.urls")),
    path("products/", ProductListView.as_view(), name="product-list"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("manage/products/", ProductManageView.as_view(), name="product-manage-create"),
    path("manage/products/<int:pk>/", ProductManageView.as_view(), name="product-manage"),
    path("place-order/", PlaceOrderView.as_view(), name="place-order"),
    path("product-statistics/", ProductStatisticsView.as_view(), name="product-statistics"),
]
