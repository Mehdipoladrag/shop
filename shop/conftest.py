import io
from decimal import Decimal

import pytest
from django.core.cache import cache
from django.core.files.base import ContentFile
from PIL import Image
from rest_framework.test import APIClient

CSRF_URL = "/accounts/api/v1/customer/csrf/"
PASSWORD = "S3cure-pass!"


@pytest.fixture(autouse=True)
def isolated_settings(settings, tmp_path):
    """Local-memory cache (sessions, throttling) and a throw-away media folder per test."""
    settings.CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}
    settings.MEDIA_ROOT = str(tmp_path / "media")
    # PBKDF2 is deliberately slow; a fast hasher keeps the test suite quick.
    settings.PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
    cache.clear()
    yield
    cache.clear()


def make_image(name="photo.png", color="#335577"):
    buffer = io.BytesIO()
    Image.new("RGB", (40, 40), color).save(buffer, "PNG")
    return ContentFile(buffer.getvalue(), name=name)


@pytest.fixture
def csrf_client():
    """API client that enforces CSRF like a browser, with the token header preset."""
    client = APIClient(enforce_csrf_checks=True)
    client.get(CSRF_URL)
    sync_csrf(client)
    return client


def sync_csrf(client):
    """Copies the current csrftoken cookie into the header (it changes after login)."""
    client.defaults["HTTP_X_CSRFTOKEN"] = client.cookies["csrftoken"].value


@pytest.fixture
def user(db, django_user_model):
    return django_user_model.objects.create_user(
        username="@ali", email="ali@example.com", password=PASSWORD, first_name="علی", last_name="رضایی"
    )


@pytest.fixture
def other_user(db, django_user_model):
    return django_user_model.objects.create_user(
        username="@sara", email="sara@example.com", password=PASSWORD
    )


@pytest.fixture
def logged_in_client(csrf_client, user):
    response = csrf_client.post("/accounts/api/v1/customer/login/", {"username": user.username, "password": PASSWORD}, format="json")
    assert response.status_code == 200, response.content
    sync_csrf(csrf_client)
    return csrf_client


@pytest.fixture
def make_product(db):
    from shop.models import Brand, Category, Info, Product

    counter = {"n": 0}

    def factory(price="1000000", offer=None, number=10, **extra):
        counter["n"] += 1
        n = counter["n"]
        category, _ = Category.objects.get_or_create(
            category_code=1, defaults={"category_name": "ساعت", "category_slug": "watch", "category_pic": make_image("c.png")}
        )
        brand, _ = Brand.objects.get_or_create(brand_code=1, defaults={"brand_name": "برند", "brand_pic": make_image("b.png")})
        info, _ = Info.objects.get_or_create(product_info="ارسال رایگان")
        return Product.objects.create(
            product_code=n, product_name=f"محصول {n}", product_color="مشکی",
            product_category=category, product_brand=brand, product_number=number,
            capability="x", resolution=12, technology="x", platform_os="x", bluetooth="دارد",
            product_rate=Decimal("4.5"), specifications="x", product_description="x", mini_description="x",
            price=Decimal(price), offer=offer, time_send=2, product_inf=info, slug=f"p-{n}",
            pic=make_image(f"p{n}.png"), **extra,
        )

    return factory
