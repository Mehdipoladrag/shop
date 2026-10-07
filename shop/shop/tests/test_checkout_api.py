from decimal import Decimal

import pytest
from rest_framework.test import APIClient

from conftest import sync_csrf
from shop.models import Invoice, Order, OrderItem, Transaction

pytestmark = pytest.mark.django_db

CART = "/shop/api/v1/public/cart/"
CHECKOUT = "/shop/api/v1/public/checkout/"
ORDERS = "/accounts/api/v1/customer/orders/"


def add_to_cart(client, product, count=1, update=False):
    return client.post(CART, {"product_id": product.id, "product_count": count, "update": update}, format="json")


# --- cart -------------------------------------------------------------------


def test_cart_changes_require_csrf_token(make_product):
    product = make_product()
    client = APIClient(enforce_csrf_checks=True)
    assert add_to_cart(client, product).status_code == 403


def test_cart_add_update_remove(csrf_client, make_product):
    product = make_product(price="1000000", offer=10)
    data = add_to_cart(csrf_client, product, 2).json()
    assert data["total_count"] == 2
    assert Decimal(str(data["items"][0]["unit_price"])) == Decimal("900000")
    assert Decimal(str(data["total_price"])) == Decimal("1800000")

    assert add_to_cart(csrf_client, product, 3, update=True).json()["total_count"] == 3
    assert csrf_client.delete(f"{CART}{product.id}/").json()["items"] == []


def test_cart_count_is_clamped_to_nine(csrf_client, make_product):
    product = make_product()
    assert add_to_cart(csrf_client, product, 50).json()["total_count"] == 9
    assert add_to_cart(csrf_client, product, 0, update=True).json()["total_count"] == 1


def test_cart_unknown_product_and_bad_count(csrf_client, make_product):
    product = make_product()
    assert csrf_client.post(CART, {"product_id": 9999}, format="json").status_code == 404
    assert csrf_client.post(CART, {"product_id": product.id, "product_count": "x"}, format="json").status_code == 400


def test_cart_uses_current_price_not_the_price_at_add_time(csrf_client, make_product):
    product = make_product(price="1000000")
    add_to_cart(csrf_client, product)
    product.price = Decimal("2000000")
    product.save()
    assert Decimal(str(csrf_client.get(CART).json()["total_price"])) == Decimal("2000000")


def test_cart_is_per_visitor(make_product):
    product = make_product()
    first, second = APIClient(), APIClient()
    for client in (first, second):
        client.get("/accounts/api/v1/customer/csrf/")
        client.defaults["HTTP_X_CSRFTOKEN"] = client.cookies["csrftoken"].value
    first.post(CART, {"product_id": product.id}, format="json")
    assert second.get(CART).json()["total_count"] == 0


# --- checkout -------------------------------------------------------------------


def test_checkout_requires_login(csrf_client, make_product):
    add_to_cart(csrf_client, make_product())
    assert csrf_client.get(CHECKOUT).status_code == 403
    assert csrf_client.post(CHECKOUT, format="json").status_code == 403


def test_checkout_requires_csrf_token(user, make_product):
    client = APIClient(enforce_csrf_checks=True)
    client.force_login(user)
    assert client.post(CHECKOUT, format="json").status_code == 403


def test_checkout_with_empty_cart_is_rejected(logged_in_client):
    response = logged_in_client.post(CHECKOUT, format="json")
    assert response.status_code == 400
    assert not Order.objects.exists()


def test_checkout_creates_order_invoice_transaction_and_items(logged_in_client, user, make_product):
    full_price = make_product(price="1000000")
    discounted = make_product(price="333333", offer=33)
    add_to_cart(logged_in_client, full_price, 2)
    add_to_cart(logged_in_client, discounted, 3)

    response = logged_in_client.post(CHECKOUT, format="json")
    assert response.status_code == 201, response.content

    order = Order.objects.get(customer=user)
    items = {item.product_id: item for item in OrderItem.objects.filter(order=order)}
    assert items[full_price.id].product_cost == Decimal("2000000.0")
    assert items[discounted.id].product_count == 3
    # 333333 - 33% = 223333.11 per unit, 669999.33 for three, kept to one decimal.
    assert items[discounted.id].product_cost == Decimal("669999.3")
    assert items[discounted.id].discounted_price == Decimal("223333.11")

    invoice = Invoice.objects.get(order=order)
    transaction = Transaction.objects.get(invoice=invoice)
    assert transaction.status == "pending"
    assert transaction.amount == sum(item.product_cost for item in items.values())

    body = response.json()
    assert body["id"] == order.id and body["status"] == "pending"
    assert Decimal(str(body["total_cost"])) == transaction.amount
    assert len(body["items"]) == 2


def test_checkout_clears_the_cart(logged_in_client, make_product):
    add_to_cart(logged_in_client, make_product())
    logged_in_client.post(CHECKOUT, format="json")
    assert logged_in_client.get(CART).json()["total_count"] == 0
    assert logged_in_client.post(CHECKOUT, format="json").status_code == 400


def test_checkout_rejects_totals_the_database_cannot_store(logged_in_client, make_product):
    huge = make_product(price="150000000")
    add_to_cart(logged_in_client, huge, 9)
    assert logged_in_client.post(CHECKOUT, format="json").status_code == 400
    assert not Order.objects.exists()


def test_checkout_get_reports_whether_the_address_is_complete(logged_in_client, make_product):
    add_to_cart(logged_in_client, make_product())
    data = logged_in_client.get(CHECKOUT).json()
    assert data["address_complete"] is False
    assert data["cart"]["total_count"] == 1

    address = {"address": "تهران", "zipcode": "1234567890", "street": "ولیعصر", "city": "تهران", "mobile": "09121234567"}
    assert logged_in_client.put("/accounts/api/v1/customer/address/", address, format="json").status_code == 200
    assert logged_in_client.get(CHECKOUT).json()["address_complete"] is True


def test_order_ignores_client_supplied_prices(logged_in_client, make_product):
    product = make_product(price="1000000")
    add_to_cart(logged_in_client, product)
    logged_in_client.post(CHECKOUT, {"total": 1, "price": 1, "product_cost": 1}, format="json")
    assert OrderItem.objects.get().product_cost == Decimal("1000000.0")


# --- orders (customer area) ------------------------------------------------------


def place_order(client, product, count=1):
    add_to_cart(client, product, count)
    return client.post(CHECKOUT, format="json").json()


def test_orders_require_login(csrf_client):
    for path in (ORDERS, f"{ORDERS}latest/", f"{ORDERS}1/"):
        assert csrf_client.get(path).status_code == 403


def test_order_list_only_contains_own_orders_newest_first(logged_in_client, other_user, make_product):
    product = make_product()
    first = place_order(logged_in_client, product)
    second = place_order(logged_in_client, product, 2)
    foreign = Order.objects.create(customer=other_user)

    results = logged_in_client.get(ORDERS).json()["results"]
    assert [order["id"] for order in results] == [second["id"], first["id"]]
    assert foreign.id not in [order["id"] for order in results]


def test_order_list_is_paginated(logged_in_client, user, make_product):
    for _ in range(12):
        Order.objects.create(customer=user)
    data = logged_in_client.get(ORDERS).json()
    assert data["count"] == 12 and len(data["results"]) == 10 and data["next"]


def test_order_detail_hides_other_customers_orders(logged_in_client, other_user):
    foreign = Order.objects.create(customer=other_user)
    assert logged_in_client.get(f"{ORDERS}{foreign.id}/").status_code == 404


def test_order_detail_and_status(logged_in_client, user, make_product):
    placed = place_order(logged_in_client, make_product())
    data = logged_in_client.get(f"{ORDERS}{placed['id']}/").json()
    assert data["status"] == "pending" and data["status_label"] == "انتظار"

    Transaction.objects.filter(invoice__order_id=placed["id"]).update(status="completed")
    assert logged_in_client.get(f"{ORDERS}{placed['id']}/").json()["status"] == "completed"


def test_latest_order(logged_in_client, make_product):
    assert logged_in_client.get(f"{ORDERS}latest/").status_code == 404
    place_order(logged_in_client, make_product())
    second = place_order(logged_in_client, make_product())
    assert logged_in_client.get(f"{ORDERS}latest/").json()["id"] == second["id"]


def test_order_with_deleted_product_still_serializes(logged_in_client, make_product):
    product = make_product()
    placed = place_order(logged_in_client, product)
    product.delete()
    item = logged_in_client.get(f"{ORDERS}{placed['id']}/").json()["items"][0]
    assert item["product_name"] == "" and item["product_slug"] == ""
