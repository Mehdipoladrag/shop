from decimal import Decimal

from rest_framework import serializers

from blog.models import Blogs
from shop.models import Brand, Category, Product

HUNDRED = Decimal(100)


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
        if not product.offer:
            return product.price
        return product.price - product.price * Decimal(product.offer) / HUNDRED


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
