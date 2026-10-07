from django.urls import path
from .checkout_views import CheckoutApiView
from .public_views import (
    PublicBlogCategoryListApiView,
    PublicBlogDetailApiView,
    PublicBlogListApiView,
    PublicBrandListApiView,
    PublicCartApiView,
    PublicCartItemApiView,
    PublicCategoryListApiView,
    PublicContactApiView,
    PublicProductDetailApiView,
    PublicProductFiltersApiView,
    PublicProductListApiView,
    PublicSessionApiView,
)
from .views import (
    # Category
    CategoryGetApiView,
    CategoryPutDeleteApiView,
    CategoryCreateApiView,
    CategoryDetailApiView,
    # Brand
    BrandGetApiView,
    BrandCreateApiView,
    BrandDetailApiView,
    BrandPutDeleteApiView,
    # product
    ProductGetApiView,
    ProductCreateApiView,
    ProductDetailApiView,
    ProductPutDeleteApiView,
    # Order
    OrderGetApiView,
    OrderDetailApiView,
    OrderPutDeleteApiView,
    # Order Item
    OrderItemGetApiView,
    OrderItemDetailApiView,
    OrderItemPutDeleteApiView,
    # Invoice
    InvoiceGetApiView,
    InvoiceDetailApiView,
    InvoicePutDeleteApiView,
    # Transaction
    TransactionGetApiView,
    TransactionDetailApiView,
    TransactionPutDeleteApiView,
)


urlpatterns = [
    # Public storefront routes (read-only, no authentication)
    path("public/categories/", PublicCategoryListApiView.as_view()),
    path("public/brands/", PublicBrandListApiView.as_view()),
    path("public/products/", PublicProductListApiView.as_view()),
    path("public/products/filters/", PublicProductFiltersApiView.as_view()),
    path("public/products/<slug:slug>/", PublicProductDetailApiView.as_view()),
    path("public/cart/", PublicCartApiView.as_view()),
    path("public/checkout/", CheckoutApiView.as_view()),
    path("public/cart/<int:product_id>/", PublicCartItemApiView.as_view()),
    path("public/contact/", PublicContactApiView.as_view()),
    path("public/session/", PublicSessionApiView.as_view()),
    path("public/blog/", PublicBlogListApiView.as_view()),
    path("public/blog/categories/", PublicBlogCategoryListApiView.as_view()),
    path("public/blog/<slug:slug>/", PublicBlogDetailApiView.as_view()),
    # Category Api Route
    path("category-list/", CategoryGetApiView.as_view()),
    path("category-create/", CategoryCreateApiView.as_view()),
    path("category-detail/<pk>/", CategoryDetailApiView.as_view()),
    path("category-data/<pk>/", CategoryPutDeleteApiView.as_view()),
    # Brand Api Route
    path("brand-list/", BrandGetApiView.as_view()),
    path("brand-create/", BrandCreateApiView.as_view()),
    path("brand-detail/<pk>/", BrandDetailApiView.as_view()),
    path("brand-data/<pk>/", BrandPutDeleteApiView.as_view()),
    # Product Api Route
    path("product-list/", ProductGetApiView.as_view()),
    path("product-create/", ProductCreateApiView.as_view()),
    path("product-detail/<pk>/", ProductDetailApiView.as_view()),
    path("product-data/<pk>/", ProductPutDeleteApiView.as_view()),
    # Order Api Route
    path("order-list/", OrderGetApiView.as_view()),
    path("order-detail/<pk>/", OrderDetailApiView.as_view()),
    path("order-data/<pk>/", OrderPutDeleteApiView.as_view()),
    # OrderItem Api Route
    path("orderitem-list/", OrderItemGetApiView.as_view()),
    path("orderitem-detail/<pk>/", OrderItemDetailApiView.as_view()),
    path("orderitem-data/<pk>/", OrderItemPutDeleteApiView.as_view()),
    # Invoice Api Route
    path("invoice-list/", InvoiceGetApiView.as_view()),
    path("invoice-detail/<pk>/", InvoiceDetailApiView.as_view()),
    path("invoice-data/<pk>/", InvoicePutDeleteApiView.as_view()),
    # Transaction Api Route
    path("transaction-list/", TransactionGetApiView.as_view()),
    path("transaction-detail/<pk>/", TransactionDetailApiView.as_view()),
    path("transaction-data/<pk>/", TransactionPutDeleteApiView.as_view()),
]
