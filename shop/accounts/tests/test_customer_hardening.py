"""Regression tests for problems found in the review of the customer API."""
import os
import subprocess
import sys
from pathlib import Path

import pytest
from django.core.files.base import ContentFile
from django.test import Client
from rest_framework.test import APIClient

from accounts.models import CustomProfileModel
from conftest import PASSWORD, make_image

pytestmark = pytest.mark.django_db

BASE = "/accounts/api/v1/customer"
PROJECT_ROOT = Path(__file__).resolve().parents[2]

REGISTER = {
    "username": "@new_user",
    "email": "new@example.com",
    "first_name": "نرگس",
    "last_name": "احمدی",
    "password1": PASSWORD,
    "password2": PASSWORD,
}


# --- throttling -----------------------------------------------------------------------------


def test_login_throttle_cannot_be_bypassed_with_a_forged_forwarded_for_header(csrf_client, user):
    statuses = [
        csrf_client.post(
            f"{BASE}/login/",
            {"username": user.username, "password": "bad"},
            format="json",
            HTTP_X_FORWARDED_FOR=f"10.0.0.{n}",
        ).status_code
        for n in range(12)
    ]
    assert 429 in statuses[10:], statuses


def test_admin_jwt_login_is_throttled_too(user):
    client = APIClient()
    statuses = [
        client.post("/accounts/api/v1/login/", {"username": user.username, "password": "bad"}, format="json").status_code
        for _ in range(12)
    ]
    assert statuses[:10] == [401] * 10 or set(statuses[:10]) <= {400, 401}
    assert 429 in statuses[10:], statuses


# --- registration rules ----------------------------------------------------------------------


@pytest.mark.parametrize("username", ["@", "@ab", "@ali​", "@‮alice", "@علی_رضا", "@a b c", "@" + "a" * 30])
def test_register_rejects_unsafe_usernames(csrf_client, username):
    response = csrf_client.post(f"{BASE}/register/", {**REGISTER, "username": username}, format="json")
    assert response.status_code == 400 and "username" in response.json()


@pytest.mark.parametrize("username", ["@ali", "@ali_reza.7", "@A1b2c3"])
def test_register_accepts_plain_usernames(csrf_client, username):
    response = csrf_client.post(f"{BASE}/register/", {**REGISTER, "username": username}, format="json")
    assert response.status_code == 201, response.content


# --- profile fields ----------------------------------------------------------------------------


@pytest.mark.parametrize("field", ["first_name", "last_name", "email"])
def test_required_account_fields_cannot_be_emptied(logged_in_client, user, field):
    before = getattr(user, field)
    response = logged_in_client.patch(f"{BASE}/profile/", {field: ""}, format="multipart")
    assert response.status_code == 400 and field in response.json()
    user.refresh_from_db()
    assert getattr(user, field) == before


def test_persian_digits_are_stored_as_ascii_digits(logged_in_client, user):
    response = logged_in_client.patch(
        f"{BASE}/profile/",
        {"mobile": "۰۹۱۲۳۴۵۶۷۸۹", "zipcode": "۱۲۳۴۵۶۷۸۹۰", "national_code": "٠٠١٢٣٤٥٦٧٨", "card_number": "۶۰۳۷۹۹۱۲۳۴۵۶۷۸۹۰"},
        format="json",
    )
    assert response.status_code == 200, response.content
    profile = CustomProfileModel.objects.get(user=user)
    assert (profile.mobile, profile.zipcode, profile.national_code, profile.card_number) == (
        "09123456789", "1234567890", "0012345678", "6037991234567890",
    )


def test_address_endpoint_normalizes_digits_too(logged_in_client, user):
    address = {"address": "تهران", "zipcode": "۱۲۳۴۵۶۷۸۹۰", "street": "x", "city": "تهران", "mobile": "۰۹۱۲۱۲۳۴۵۶۷"}
    assert logged_in_client.put(f"{BASE}/address/", address, format="json").status_code == 200
    assert CustomProfileModel.objects.get(user=user).mobile == "09121234567"


def test_a_full_iranian_iban_fits(logged_in_client, user):
    iban = "IR" + "0" * 24
    assert len(iban) == 26
    assert logged_in_client.patch(f"{BASE}/profile/", {"iban": iban}, format="json").status_code == 200
    assert logged_in_client.patch(f"{BASE}/profile/", {"iban": iban + "0"}, format="json").status_code == 400


# --- profile picture -----------------------------------------------------------------------------


def test_oversized_profile_pictures_are_rejected(logged_in_client):
    import io
    from PIL import Image

    buffer = io.BytesIO()
    Image.new("RGB", (40, 40)).save(buffer, "PNG")
    big = ContentFile(buffer.getvalue() + b"\0" * (2 * 1024 * 1024 + 10), name="big.png")
    response = logged_in_client.patch(f"{BASE}/profile/", {"customer_image": big}, format="multipart")
    assert response.status_code == 400 and "customer_image" in response.json()


def test_replacing_the_picture_deletes_the_old_file(logged_in_client, user):
    logged_in_client.patch(f"{BASE}/profile/", {"customer_image": make_image("first.png")}, format="multipart")
    first = CustomProfileModel.objects.get(user=user).customer_image
    first_path = Path(first.path)
    assert first_path.exists()

    logged_in_client.patch(f"{BASE}/profile/", {"customer_image": make_image("second.png", "#aa3355")}, format="multipart")
    assert not first_path.exists(), "the replaced picture must not stay on disk"
    assert Path(CustomProfileModel.objects.get(user=user).customer_image.path).exists()


# --- CSRF failure page ---------------------------------------------------------------------------


def test_api_csrf_failures_are_json_but_admin_pages_keep_html(db):
    api = APIClient(enforce_csrf_checks=True).post(f"{BASE}/login/", {}, format="json")
    assert api.status_code == 403 and api["Content-Type"].startswith("application/json")

    admin = Client(enforce_csrf_checks=True).post("/admin/login/", {"username": "x", "password": "y"})
    assert admin.status_code == 403 and admin["Content-Type"].startswith("text/html")


# --- SECRET_KEY ----------------------------------------------------------------------------------


def load_settings(**env):
    """Imports the settings in a fresh interpreter, like a production process would."""
    clean = {k: v for k, v in os.environ.items() if k not in {"DEBUG", "SECRET_KEY"}}
    clean.update(env, DJANGO_SETTINGS_MODULE="shopproject.settings")
    return subprocess.run(
        [sys.executable, "-c", "from django.conf import settings; print(len(settings.SECRET_KEY))"],
        cwd=PROJECT_ROOT, env=clean, capture_output=True, text=True,
    )


def test_production_refuses_to_start_without_a_secret_key():
    result = load_settings()
    assert result.returncode != 0 and "SECRET_KEY" in result.stderr


def test_secret_key_from_the_environment_is_used():
    assert load_settings(SECRET_KEY="x" * 50).returncode == 0


def test_local_development_may_use_the_built_in_key():
    assert load_settings(DEBUG="True").returncode == 0
