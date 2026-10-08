import pytest
from django.core.management import call_command

from blog.models import Blogs
from shop.models import Brand, Category, Product

pytestmark = pytest.mark.django_db


def test_catalog_seed_creates_priced_products_with_pictures():
    call_command("seed_demo_catalog")

    products = Product.objects.all()
    assert products.count() == 16
    assert Category.objects.filter(category_slug__in=["mobile", "gaming"]).count() == 2
    assert Brand.objects.filter(brand_name="Apple").exists()
    for product in products:
        assert product.pic and product.price > 0
        assert 0 <= product.offer <= 100


def test_catalog_seed_can_run_twice():
    call_command("seed_demo_catalog")
    call_command("seed_demo_catalog")

    assert Product.objects.count() == 16


def test_blog_seed_creates_posts_once():
    call_command("seed_demo_blog")
    call_command("seed_demo_blog")

    assert Blogs.objects.filter(slug__in=["how-to-choose-iphone", "iphone-14-vs-13", "iphone-care-tips"]).count() == 3
