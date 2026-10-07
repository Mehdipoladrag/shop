from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from shop.models import Brand, Category, Product

from .public_serializers import (
    PublicBrandSerializer,
    PublicCategorySerializer,
    PublicProductDetailSerializer,
    PublicProductListSerializer,
)

RELATED_PRODUCTS_LIMIT = 4

# Sort keys accepted by the `ordering` query parameter.
ALLOWED_ORDERINGS = {"price", "-price", "-create_date", "-product_rate"}


class PublicApiMixin:
    """Read-only endpoints open to everyone, with no credentials required."""

    permission_classes = [AllowAny]
    authentication_classes = []


class ProductPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = "page_size"
    max_page_size = 48


class PublicCategoryListApiView(PublicApiMixin, generics.ListAPIView):
    queryset = Category.objects.order_by("category_code")
    serializer_class = PublicCategorySerializer
    pagination_class = None

    @swagger_auto_schema(tags=["Storefront"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class PublicBrandListApiView(PublicApiMixin, generics.ListAPIView):
    queryset = Brand.objects.order_by("brand_code")
    serializer_class = PublicBrandSerializer
    pagination_class = None

    @swagger_auto_schema(tags=["Storefront"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class PublicProductListApiView(PublicApiMixin, generics.ListAPIView):
    """
    Paginated product list.

    Query parameters: `category` (slug), `search` (name), `has_offer=1`,
    `ordering` (price, -price, -create_date, -product_rate).
    """

    serializer_class = PublicProductListSerializer
    pagination_class = ProductPagination

    def get_queryset(self):
        params = self.request.query_params
        queryset = Product.objects.select_related("product_category", "product_brand")

        category_slug = params.get("category")
        if category_slug:
            queryset = queryset.filter(product_category__category_slug=category_slug)

        search = params.get("search", "").strip()
        if search:
            queryset = queryset.filter(
                Q(product_name__icontains=search) | Q(mini_description__icontains=search)
            )

        if params.get("has_offer") == "1":
            queryset = queryset.filter(offer__gt=0)

        ordering = params.get("ordering")
        # Unknown values fall back to newest first instead of raising an error.
        return queryset.order_by(ordering if ordering in ALLOWED_ORDERINGS else "-create_date")

    @swagger_auto_schema(tags=["Storefront"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class PublicProductDetailApiView(PublicApiMixin, APIView):
    """One product by slug, plus other products from the same category."""

    @swagger_auto_schema(tags=["Storefront"])
    def get(self, request, slug):
        product = (
            Product.objects.select_related("product_category", "product_brand", "product_inf")
            .filter(slug=slug)
            .first()
        )
        if product is None:
            return Response({"detail": "Product not found."}, status=404)

        related = (
            Product.objects.select_related("product_category", "product_brand")
            .filter(product_category=product.product_category)
            .exclude(pk=product.pk)
            .order_by("-create_date")[:RELATED_PRODUCTS_LIMIT]
        )
        context = {"request": request}
        return Response(
            {
                "product": PublicProductDetailSerializer(product, context=context).data,
                "related": PublicProductListSerializer(related, many=True, context=context).data,
            }
        )
