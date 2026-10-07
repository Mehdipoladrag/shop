
from rest_framework import serializers

from blog.models import Blogs
from contact.models import Contact
from shop.models import Brand, Category, OrderItem, Order, Product, Transaction
from accounts.api.v1.customer_serializers import MOBILE_PATTERN, PERSIAN_TO_ASCII_DIGITS
from shop.pricing import discounted_price



class PublicCategorySerializer(serializers.ModelSerializer):
    """Category data shown on the storefront."""

    class Meta:
        model = Category
        fields = ["id", "category_name", "category_slug", "category_pic"]


class PublicBrandSerializer(serializers.ModelSerializer):
    """Brand data shown on the storefront."""

    class Meta:
        model = Brand
        fields = ["id", "brand_name", "brand_pic"]


class PublicProductListSerializer(serializers.ModelSerializer):
    """Compact product data for listings and cards."""

    category = serializers.CharField(source="product_category.category_name")
    category_slug = serializers.CharField(source="product_category.category_slug")
    brand = serializers.CharField(source="product_brand.brand_name")
    final_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "product_name",
            "slug",
            "mini_description",
            "category",
            "category_slug",
            "brand",
            "price",
            "offer",
            "final_price",
            "product_rate",
            "product_number",
            "pic",
        ]

    def get_final_price(self, product):
        """Price after the percentage discount, matching the cart logic."""
        return discounted_price(product.price, product.offer)


class PublicProductDetailSerializer(PublicProductListSerializer):
    """Everything the product page needs, including the gallery."""

    images = serializers.SerializerMethodField()
    notice = serializers.CharField(source="product_inf.product_info", default="")

    class Meta(PublicProductListSerializer.Meta):
        fields = PublicProductListSerializer.Meta.fields + [
            "product_code",
            "product_color",
            "capability",
            "resolution",
            "technology",
            "platform_os",
            "bluetooth",
            "specifications",
            "product_description",
            "time_send",
            "notice",
            "images",
        ]

    def get_images(self, product):
        """Main picture first, followed by the optional extra pictures."""
        request = self.context.get("request")
        pictures = [product.pic, product.pic2, product.pic3, product.pic4, product.pic5]
        return [
            request.build_absolute_uri(picture.url) if request else picture.url
            for picture in pictures
            if picture
        ]


class PublicBlogListSerializer(serializers.ModelSerializer):
    """Blog post card data."""

    author = serializers.CharField(source="username.username")
    category = serializers.CharField(source="category.name")
    category_slug = serializers.CharField(source="category.slug_cat")

    class Meta:
        model = Blogs
        fields = [
            "id",
            "blog_name",
            "slug",
            "blog_image",
            "author",
            "category",
            "category_slug",
            "create_date",
        ]


class PublicBlogDetailSerializer(PublicBlogListSerializer):
    class Meta(PublicBlogListSerializer.Meta):
        fields = PublicBlogListSerializer.Meta.fields + ["blog_description"]


class PublicContactSerializer(serializers.ModelSerializer):
    """Contact form submitted from the storefront."""

    phone = serializers.CharField(max_length=20)

    class Meta:
        model = Contact
        fields = ["name", "email", "phone", "subject", "desc"]

    def validate_phone(self, value):
        # The periodic cleanup task deletes contacts whose phone does not start with 09.
        phone = value.translate(PERSIAN_TO_ASCII_DIGITS)
        if not MOBILE_PATTERN.match(phone):
            raise serializers.ValidationError("شماره همراه باید با ۰۹ شروع شود و ۱۱ رقم باشد")
        return phone


class OrderItemSerializer(serializers.ModelSerializer):
    """One purchased product inside an order."""

    product_name = serializers.SerializerMethodField()
    product_slug = serializers.SerializerMethodField()
    product_pic = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product_name",
            "product_slug",
            "product_pic",
            "product_price",
            "discounted_price",
            "product_count",
            "product_cost",
        ]

    # The product is nullable: it can be deleted after the order was placed.
    def get_product_name(self, item):
        return item.product.product_name if item.product else ""

    def get_product_slug(self, item):
        return item.product.slug if item.product else ""

    def get_product_pic(self, item):
        if not item.product or not item.product.pic:
            return ""
        request = self.context.get("request")
        url = item.product.pic.url
        return request.build_absolute_uri(url) if request else url


class OrderSerializer(serializers.ModelSerializer):
    """An order of the logged in customer with its items and payment status."""

    items = OrderItemSerializer(source="orderitem_set", many=True, read_only=True)
    total_cost = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    status_label = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ["id", "order_date", "total_cost", "status", "status_label", "items"]

    def get_total_cost(self, order):
        return sum(item.product_cost for item in order.orderitem_set.all())

    def get_status(self, order):
        transaction = (
            Transaction.objects.filter(invoice__order=order).order_by("-id").first()
        )
        return transaction.status if transaction else "pending"

    def get_status_label(self, order):
        return dict(Transaction.STATUS_CHOICE)[self.get_status(order)]
