from decimal import Decimal

from django.db.models import DecimalField, ExpressionWrapper, F, Max, Min, Q, Value
from django.db.models.functions import Coalesce, Greatest, Least
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView

from blog.models import Blogs, Category_blog
from cart.cart import Cart
from shop.models import Brand, Category, Product
from shopproject.security import CsrfProtectedMixin

from .public_serializers import (
    PublicBlogDetailSerializer,
    PublicBlogListSerializer,
    PublicBrandSerializer,
    PublicCategorySerializer,
    PublicContactSerializer,
    PublicProductDetailSerializer,
    PublicProductListSerializer,
)

RELATED_PRODUCTS_LIMIT = 4

# Sort keys accepted by the `ordering` query parameter. Price sorting uses the
# discounted price, which is what the customer sees.
ALLOWED_ORDERINGS = {"final", "-final", "-create_date", "-product_rate", "time_send"}
ORDERING_ALIASES = {"price": "final", "-price": "-final"}

# Same bounds as the quantity selector of the existing cart form.
MIN_CART_COUNT = 1
MAX_CART_COUNT = 9

# Values that mean "true" for a flag sent as JSON or form data.
TRUE_VALUES = (True, 1, "1", "true", "True")

PRICE_FIELD = DecimalField(max_digits=14, decimal_places=2)
# Same clamp as shop.pricing.clamp_offer, evaluated by the database.
OFFER_PERCENT = Least(Greatest(Coalesce("offer", Value(0)), Value(0)), Value(100))
FINAL_PRICE = ExpressionWrapper(
    F("price") * (Value(100) - OFFER_PERCENT) / Value(100),
    output_field=PRICE_FIELD,
)

# Limits that keep hostile query values away from the database.
MAX_FILTER_PRICE = Decimal(10) ** 12
MAX_ID_DIGITS = 18


def parse_decimal(value):
    """Returns a finite Decimal for a query parameter, or None when it is missing, invalid or absurd."""
    try:
        number = Decimal(value)
    except (TypeError, ValueError, ArithmeticError):
        return None
    if not number.is_finite() or abs(number) > MAX_FILTER_PRICE:
        return None
    return number


def parse_int_list(value):
    """Turns "1,2,x" into [1, 2]; items that are not plain ASCII digits are ignored."""
    ids = []
    for item in (value or "").split(","):
        item = item.strip()
        if item.isascii() and item.isdigit() and len(item) <= MAX_ID_DIGITS:
            ids.append(int(item))
    return ids


def clean_text(value):
    """Query text without NUL bytes, which PostgreSQL cannot store or compare."""
    return (value or "").replace("\x00", "").strip()


class PublicApiMixin:
    """Read-only endpoints open to everyone, with no credentials required."""

    permission_classes = [AllowAny]
    authentication_classes = []


class ProductPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = "page_size"
    max_page_size = 48


class BlogPagination(PageNumberPagination):
    page_size = 6


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

    Query parameters: `category` (slug), `search` (name), `brand` (comma
    separated ids), `color` (comma separated), `min_price` / `max_price`
    (discounted price), `has_offer=1`, `in_stock=1`, `ordering` (price,
    -price, -create_date, -product_rate, time_send).
    """

    serializer_class = PublicProductListSerializer
    pagination_class = ProductPagination

    def get_queryset(self):
        params = self.request.query_params
        queryset = Product.objects.select_related("product_category", "product_brand").annotate(
            final=FINAL_PRICE
        )

        category_slug = clean_text(params.get("category"))
        if category_slug:
            queryset = queryset.filter(product_category__category_slug=category_slug)

        search = clean_text(params.get("search"))
        if search:
            queryset = queryset.filter(
                Q(product_name__icontains=search) | Q(mini_description__icontains=search)
            )

        brand_ids = parse_int_list(params.get("brand"))
        if brand_ids:
            queryset = queryset.filter(product_brand_id__in=brand_ids)

        colors = [clean_text(color) for color in params.get("color", "").split(",") if clean_text(color)]
        if colors:
            queryset = queryset.filter(product_color__in=colors)

        min_price = parse_decimal(params.get("min_price"))
        if min_price is not None:
            queryset = queryset.filter(final__gte=min_price)
        max_price = parse_decimal(params.get("max_price"))
        if max_price is not None:
            queryset = queryset.filter(final__lte=max_price)

        if params.get("has_offer") == "1":
            queryset = queryset.filter(offer__gt=0)
        if params.get("in_stock") == "1":
            queryset = queryset.filter(product_number__gt=0)

        ordering = ORDERING_ALIASES.get(params.get("ordering"), params.get("ordering"))
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


class PublicProductFiltersApiView(PublicApiMixin, APIView):
    """Values the shop sidebar needs: available colors and the price range."""

    @swagger_auto_schema(tags=["Storefront"])
    def get(self, request):
        products = Product.objects.annotate(final=FINAL_PRICE)
        price_range = products.aggregate(min_price=Min("final"), max_price=Max("final"))
        colors = products.order_by("product_color").values_list("product_color", flat=True).distinct()
        return Response(
            {
                "colors": [color for color in colors if color],
                "min_price": price_range["min_price"] or 0,
                "max_price": price_range["max_price"] or 0,
            }
        )


def serialize_cart(request):
    """Cart contents with prices, for the cart page and the header."""
    lines = Cart(request).lines()
    items = [
        {
            "product": PublicProductListSerializer(line["product"], context={"request": request}).data,
            "product_color": line["product"].product_color,
            "product_count": line["product_count"],
            "unit_price": line["unit_price"],
            "total_price": line["total_price"],
        }
        for line in lines
    ]
    return {
        "items": items,
        "total_count": sum(line["product_count"] for line in lines),
        "total_price": sum((line["total_price"] for line in lines), Decimal(0)),
    }


class PublicCartApiView(CsrfProtectedMixin, PublicApiMixin, APIView):
    """
    Shopping cart stored in the Django session. The session cookie identifies
    the visitor, and checkout reads the same cart. Changes need a CSRF token.
    """

    @swagger_auto_schema(tags=["Storefront"])
    def get(self, request):
        return Response(serialize_cart(request))

    @swagger_auto_schema(tags=["Storefront"])
    def post(self, request):
        """Adds a product, or replaces its count when `update` is true."""
        data = request.data
        if not isinstance(data, dict):
            return Response({"detail": "Invalid request body."}, status=400)

        product_ids = parse_int_list(str(data.get("product_id")))
        product = Product.objects.filter(pk=product_ids[0]).first() if product_ids else None
        if product is None:
            return Response({"detail": "Product not found."}, status=404)

        try:
            count = int(data.get("product_count", 1))
        except (TypeError, ValueError, OverflowError):
            return Response({"detail": "Invalid product count."}, status=400)

        cart = Cart(request)
        existing = cart.cart.get(str(product.id), {}).get("product_count", 0)
        update = data.get("update") in TRUE_VALUES
        new_count = count if update else existing + count
        cart.add(
            product=product,
            product_count=max(MIN_CART_COUNT, min(new_count, MAX_CART_COUNT)),
            update_count=True,
        )
        return Response(serialize_cart(request))


class PublicCartItemApiView(CsrfProtectedMixin, PublicApiMixin, APIView):
    @swagger_auto_schema(tags=["Storefront"])
    def delete(self, request, product_id):
        Cart(request).remove(product_id)
        return Response(serialize_cart(request))


class PublicBlogListApiView(PublicApiMixin, generics.ListAPIView):
    """Paginated blog posts, optionally filtered by `category` (slug)."""

    serializer_class = PublicBlogListSerializer
    pagination_class = BlogPagination

    def get_queryset(self):
        queryset = Blogs.objects.select_related("username", "category").order_by("-create_date")
        category_slug = clean_text(self.request.query_params.get("category"))
        if category_slug:
            queryset = queryset.filter(category__slug_cat=category_slug)
        return queryset

    @swagger_auto_schema(tags=["Storefront"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class PublicBlogDetailApiView(PublicApiMixin, APIView):
    @swagger_auto_schema(tags=["Storefront"])
    def get(self, request, slug):
        post = Blogs.objects.select_related("username", "category").filter(slug=slug).first()
        if post is None:
            return Response({"detail": "Post not found."}, status=404)
        return Response(PublicBlogDetailSerializer(post, context={"request": request}).data)


class PublicBlogCategoryListApiView(PublicApiMixin, APIView):
    @swagger_auto_schema(tags=["Storefront"])
    def get(self, request):
        categories = Category_blog.objects.order_by("name")
        return Response([{"id": c.id, "name": c.name, "slug": c.slug_cat} for c in categories])


class ContactThrottle(AnonRateThrottle):
    """Keeps the public contact form from being used to flood the inbox."""

    rate = "10/hour"


class PublicContactApiView(PublicApiMixin, generics.CreateAPIView):
    serializer_class = PublicContactSerializer
    throttle_classes = [ContactThrottle]

    @swagger_auto_schema(tags=["Storefront"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class PublicSessionApiView(PublicApiMixin, APIView):
    """Tells the storefront whether the visitor is logged in through the Django site."""

    # Reads the Django session cookie. The endpoint is read-only, so no CSRF risk.
    authentication_classes = [SessionAuthentication]

    @swagger_auto_schema(tags=["Storefront"])
    def get(self, request):
        user = request.user
        return Response(
            {
                "is_authenticated": user.is_authenticated,
                "username": user.get_username() if user.is_authenticated else "",
            }
        )
