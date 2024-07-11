from django.urls import path, include
from shop.views import (
    ShopListView,
    ShopDetailView,
    SearchView,
    CategoryListView,
    CategoryDetailView,
    CheckOutView,
)

app_name = "shop"

urlpatterns = [
    path("", ShopListView.as_view(), name="shoplist"),
    path("search/", SearchView.as_view(), name="search1"),
    path("product/<slug:slug>/", ShopDetailView.as_view(), name="detailpro"),
    path("all-categories/", CategoryListView.as_view(), name="categorylist1"),
    path("<str:category_slug>/", CategoryDetailView.as_view(), name="categorydetail1"),
    path("payment/checkout/", CheckOutView.as_view(), name="checkout1"),
    path("api/v1/", include("shop.api.v1.urls")),
]
