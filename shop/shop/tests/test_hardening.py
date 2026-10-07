"""Regression tests for problems found in the review of the cart and checkout."""
from decimal import Decimal

import pytest
from django.core.cache import cache
from django.conf import settings
from django.contrib.sessions.backends.cache import SessionStore
from rest_framework.test import APIClient

from conftest import sync_csrf
from shop.api.v1 import checkout_views
from shop.models import Order, OrderItem

pytestmark = pytest.mark.django_db

CART = "/shop/api/v1/public/cart/"
CHECKOUT = "/shop/api/v1/public/checkout/"
PRODUCTS = "/shop/api/v1/public/products/"
BLOG = "/shop/api/v1/public/blog/"


def add(client, product, count=1):
    return client.post(CART, {"product_id": product.id, "product_count": count}, format="json")


# --- the cart does not create sessions by itself ---------------------------------------


def test_reading_the_cart_does_not_create_a_session():
    client = APIClient()
    client.get(CART)
    assert "sessionid" not in client.cookies and settings.SESSION_COOKIE_NAME not in client.cookies


def test_cart_is_still_kept_between_requests_once_something_was_added(csrf_client, make_product):
    add(csrf_client, make_product())
    assert csrf_client.get(CART).json()["total_count"] == 1


# --- malformed input answers 4xx, never 500 ---------------------------------------------


@pytest.fixture
def lenient_client(csrf_client):
    """Returns responses instead of re-raising server errors, so a 500 shows up as a status."""
    csrf_client.raise_request_exception = False
    return csrf_client


def post_raw(client, raw_json):
    """Sends the text as the request body, exactly as a hostile client could."""
    return client.post(CART, data=raw_json, content_type="application/json")


@pytest.mark.parametrize("raw", ["[1, 2]", '"text"', "5", "null"])
def test_cart_rejects_bodies_that_are_not_objects(lenient_client, raw):
    assert post_raw(lenient_client, raw).status_code == 400


@pytest.mark.parametrize(
    "raw",
    ['{"product_id": 1, "product_count": 1e999}', '{"product_id": "²"}', '{"product_id": "' + "9" * 5000 + '"}'],
)
def test_cart_survives_hostile_numbers(lenient_client, make_product, raw):
    make_product()
    assert post_raw(lenient_client, raw).status_code in (400, 404)


def test_cart_update_flag_is_parsed_strictly(csrf_client, make_product):
    product = make_product()
    add(csrf_client, product, 5)
    csrf_client.post(CART, {"product_id": product.id, "product_count": 1, "update": "false"}, format="json")
    assert csrf_client.get(CART).json()["total_count"] == 6, '"false" must not count as true'


@pytest.mark.parametrize(
    "query",
    ["min_price=NaN", "min_price=Infinity", "max_price=-Infinity", "min_price=1e999999", "brand=²", "category=%00", "search=%00", "color=%00", "brand=" + "9" * 5000],
)
def test_product_filters_ignore_hostile_values(lenient_client, make_product, query):
    make_product()
    assert lenient_client.get(f"{PRODUCTS}?{query}").status_code == 200


def test_blog_category_filter_survives_a_nul_byte(lenient_client):
    assert lenient_client.get(f"{BLOG}?category=%00").status_code == 200


# --- discounts are percentages between 0 and 100 -----------------------------------------


@pytest.mark.parametrize("offer, expected_unit", [(150, "0"), (-30, "1000000"), (None, "1000000"), (100, "0"), (25, "750000")])
def test_offers_outside_zero_to_hundred_are_clamped(csrf_client, make_product, offer, expected_unit):
    add(csrf_client, make_product(price="1000000", offer=offer))
    item = csrf_client.get(CART).json()["items"][0]
    assert Decimal(str(item["unit_price"])) == Decimal(expected_unit)
    assert Decimal(str(item["product"]["final_price"])) == Decimal(expected_unit)


def test_price_sorting_clamps_offers_too(csrf_client, make_product):
    cheap = make_product(price="1000", offer=500)
    dear = make_product(price="1000", offer=None)
    slugs = [p["slug"] for p in csrf_client.get(f"{PRODUCTS}?ordering=price").json()["results"]]
    assert slugs == [cheap.slug, dear.slug]


# --- checkout ----------------------------------------------------------------------------


def test_checkout_accepts_expensive_products(logged_in_client, make_product):
    product = make_product(price="150000000")
    add(logged_in_client, product)
    response = logged_in_client.post(CHECKOUT, format="json")
    assert response.status_code == 201, response.content
    assert OrderItem.objects.get().discounted_price == Decimal("150000000.00")


def test_a_running_checkout_blocks_a_second_one(logged_in_client, user, make_product):
    add(logged_in_client, make_product())
    assert checkout_views.acquire_checkout_lock(user.pk)  # another request holds the lock
    response = logged_in_client.post(CHECKOUT, format="json")
    assert response.status_code == 409
    assert not Order.objects.exists()


def test_the_lock_is_released_after_the_checkout(logged_in_client, user, make_product):
    add(logged_in_client, make_product())
    assert logged_in_client.post(CHECKOUT, format="json").status_code == 201
    assert checkout_views.acquire_checkout_lock(user.pk), "a finished checkout must free the lock"


def test_the_lock_is_released_when_the_checkout_fails(logged_in_client, user):
    assert logged_in_client.post(CHECKOUT, format="json").status_code == 400  # empty cart
    assert checkout_views.acquire_checkout_lock(user.pk)


def test_a_waiting_checkout_does_not_reuse_a_cart_that_was_just_ordered(logged_in_client, make_product, monkeypatch):
    """The request authenticates (loading the session) before it gets the lock; if another
    checkout empties the cart in between, the stale copy must not be ordered again."""
    add(logged_in_client, make_product())
    session_key = logged_in_client.session.session_key
    original = checkout_views.acquire_checkout_lock

    def acquire_after_the_other_request_finished(user_id):
        store = SessionStore(session_key=session_key)
        store[settings.CART_SESSION_ID] = {}  # what the first checkout did
        store.save()
        return original(user_id)

    monkeypatch.setattr(checkout_views, "acquire_checkout_lock", acquire_after_the_other_request_finished)
    response = logged_in_client.post(CHECKOUT, format="json")
    assert response.status_code == 400
    assert not Order.objects.exists()
