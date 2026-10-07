import pytest
from rest_framework.test import APIClient

from accounts.models import CustomProfileModel
from conftest import PASSWORD, make_image, sync_csrf

pytestmark = pytest.mark.django_db

BASE = "/accounts/api/v1/customer"

REGISTER = {
    "username": "@new_user",
    "email": "new@example.com",
    "first_name": "نرگس",
    "last_name": "احمدی",
    "password1": PASSWORD,
    "password2": PASSWORD,
}


def post(client, path, data=None, **kwargs):
    return client.post(f"{BASE}/{path}/", data or {}, format="json", **kwargs)


# --- CSRF ---------------------------------------------------------------


def test_csrf_endpoint_sets_cookie():
    client = APIClient()
    response = client.get(f"{BASE}/csrf/")
    assert response.status_code == 200
    assert client.cookies["csrftoken"].value


@pytest.mark.parametrize("path", ["register", "login", "logout"])
def test_state_changing_endpoints_reject_missing_csrf_token(path):
    client = APIClient(enforce_csrf_checks=True)
    response = post(client, path, REGISTER)
    assert response.status_code == 403
    assert response.json()["detail"]


# --- registration ---------------------------------------------------------


def test_register_creates_user_and_profile(csrf_client, django_user_model):
    response = post(csrf_client, "register", REGISTER)
    assert response.status_code == 201
    user = django_user_model.objects.get(username="@new_user")
    assert user.check_password(PASSWORD) and user.password != PASSWORD
    assert CustomProfileModel.objects.filter(user=user).exists()
    assert not user.is_staff and not user.is_superuser


@pytest.mark.parametrize(
    "changes, field",
    [
        ({"username": "no_at_sign"}, "username"),
        ({"username": "1@digit"}, "username"),
        ({"email": "not-an-email"}, "email"),
        ({"password1": "short", "password2": "short"}, "password1"),
        ({"password2": "different-pass1"}, "password2"),
        ({"first_name": ""}, "first_name"),
    ],
)
def test_register_validation(csrf_client, changes, field):
    response = post(csrf_client, "register", {**REGISTER, **changes})
    assert response.status_code == 400
    assert field in response.json()


def test_register_rejects_duplicates_case_insensitively(csrf_client, user):
    duplicate_name = post(csrf_client, "register", {**REGISTER, "username": "@ALI"})
    duplicate_email = post(csrf_client, "register", {**REGISTER, "email": "ALI@example.com"})
    assert "username" in duplicate_name.json()
    assert "email" in duplicate_email.json()


def test_register_error_messages_are_persian(csrf_client):
    response = post(csrf_client, "register", {})
    assert response.json()["username"] == ["لطفاً این فیلد را پر کنید"]


def test_register_cannot_set_staff_flags(csrf_client, django_user_model):
    post(csrf_client, "register", {**REGISTER, "is_staff": True, "is_superuser": True})
    user = django_user_model.objects.get(username="@new_user")
    assert not user.is_staff and not user.is_superuser


# --- login / logout ------------------------------------------------------------


def test_login_success_starts_session_and_rotates_csrf(csrf_client, user):
    old_token = csrf_client.cookies["csrftoken"].value
    response = post(csrf_client, "login", {"username": user.username, "password": PASSWORD})
    assert response.status_code == 200
    assert response.json()["username"] == "@ali"
    assert csrf_client.cookies["csrftoken"].value != old_token
    assert "sessionid" in csrf_client.cookies or "massay_session_cookie" in csrf_client.cookies
    sync_csrf(csrf_client)
    assert csrf_client.get(f"{BASE}/profile/").status_code == 200


def test_login_creates_missing_profile(csrf_client, user):
    CustomProfileModel.objects.filter(user=user).delete()
    post(csrf_client, "login", {"username": user.username, "password": PASSWORD})
    assert CustomProfileModel.objects.filter(user=user).exists()


def test_login_failure_messages_do_not_reveal_which_part_was_wrong(csrf_client, user):
    wrong_password = post(csrf_client, "login", {"username": user.username, "password": "nope"})
    unknown_user = post(csrf_client, "login", {"username": "@ghost", "password": "nope"})
    assert wrong_password.status_code == unknown_user.status_code == 400
    assert wrong_password.json() == unknown_user.json()


def test_inactive_user_cannot_log_in(csrf_client, user):
    user.is_active = False
    user.save()
    response = post(csrf_client, "login", {"username": user.username, "password": PASSWORD})
    assert response.status_code == 400


def test_login_is_throttled(csrf_client, user):
    statuses = [post(csrf_client, "login", {"username": user.username, "password": "bad"}).status_code for _ in range(12)]
    assert statuses[:10] == [400] * 10
    assert 429 in statuses[10:]


def test_logout_ends_session(logged_in_client):
    assert post(logged_in_client, "logout").status_code == 204
    assert logged_in_client.get(f"{BASE}/profile/").status_code == 403


# --- profile -------------------------------------------------------------------


def test_profile_requires_login(csrf_client):
    assert csrf_client.get(f"{BASE}/profile/").status_code == 403
    assert csrf_client.patch(f"{BASE}/profile/", {}, format="json").status_code == 403


def test_profile_get_returns_user_and_profile_fields(logged_in_client):
    data = logged_in_client.get(f"{BASE}/profile/").json()
    assert data["username"] == "@ali" and data["first_name"] == "علی"
    assert data["is_complete"] is False


COMPLETE_PROFILE = {
    "national_code": "0012345678",
    "address": "تهران، خیابان آزادی",
    "zipcode": "1234567890",
    "street": "آزادی",
    "city": "تهران",
    "mobile": "09121234567",
    "age": 30,
    "card_number": "6037991234567890",
    "iban": "IR12345678",
}


def test_profile_patch_updates_and_marks_complete(logged_in_client, user):
    response = logged_in_client.patch(
        f"{BASE}/profile/", {**COMPLETE_PROFILE, "first_name": "محمد", "email": "mo@example.com"}, format="json"
    )
    assert response.status_code == 200, response.content
    user.refresh_from_db()
    assert (user.first_name, user.email) == ("محمد", "mo@example.com")
    assert user.profile.city == "تهران" and user.profile.is_complete is True


def test_profile_partial_update_does_not_reset_other_fields(logged_in_client, user):
    logged_in_client.patch(f"{BASE}/profile/", {"city": "شیراز", "gender": True}, format="multipart")
    logged_in_client.patch(f"{BASE}/profile/", {"age": 40}, format="multipart")
    user.profile.refresh_from_db()
    assert user.profile.city == "شیراز"
    assert user.profile.gender is True, "a multipart PATCH without gender must not reset it"


@pytest.mark.parametrize(
    "field, value",
    [
        ("national_code", "123"),
        ("zipcode", "12ab"),
        ("mobile", "12345"),
        ("card_number", "1234"),
        ("email", "broken"),
    ],
)
def test_profile_validation(logged_in_client, field, value):
    response = logged_in_client.patch(f"{BASE}/profile/", {field: value}, format="json")
    assert response.status_code == 400 and field in response.json()


def test_profile_email_must_be_unique(logged_in_client, other_user):
    response = logged_in_client.patch(f"{BASE}/profile/", {"email": other_user.email}, format="json")
    assert response.status_code == 400 and "email" in response.json()


def test_profile_cannot_change_username_or_flags(logged_in_client, user):
    logged_in_client.patch(f"{BASE}/profile/", {"username": "@hacked", "is_staff": True, "is_complete": True}, format="json")
    user.refresh_from_db()
    assert user.username == "@ali" and not user.is_staff and user.profile.is_complete is False


def test_profile_image_upload(logged_in_client, user):
    response = logged_in_client.patch(f"{BASE}/profile/", {"customer_image": make_image()}, format="multipart")
    assert response.status_code == 200, response.content
    user.profile.refresh_from_db()
    assert user.profile.customer_image.name.startswith("images/profile/")


def test_profile_rejects_non_image_upload(logged_in_client):
    from django.core.files.uploadedfile import SimpleUploadedFile

    fake = SimpleUploadedFile("evil.png", b"<script>alert(1)</script>", content_type="image/png")
    response = logged_in_client.patch(f"{BASE}/profile/", {"customer_image": fake}, format="multipart")
    assert response.status_code == 400


def test_profile_patch_requires_csrf_token(user):
    client = APIClient(enforce_csrf_checks=True)
    client.force_login(user)
    assert client.patch(f"{BASE}/profile/", {"city": "x"}, format="json").status_code == 403


# --- password ------------------------------------------------------------------


NEW_PASSWORD = "An0ther-pass!"


def password_payload(**changes):
    return {"old_password": PASSWORD, "new_password1": NEW_PASSWORD, "new_password2": NEW_PASSWORD, **changes}


def test_change_password_keeps_session_and_new_password_works(logged_in_client, user):
    response = post(logged_in_client, "password", password_payload())
    assert response.status_code == 200
    assert logged_in_client.get(f"{BASE}/profile/").status_code == 200
    user.refresh_from_db()
    assert user.check_password(NEW_PASSWORD)


@pytest.mark.parametrize(
    "changes, field",
    [
        ({"old_password": "wrong"}, "old_password"),
        ({"new_password2": "mismatch-pass"}, "new_password2"),
        ({"new_password1": "short", "new_password2": "short"}, "new_password1"),
    ],
)
def test_change_password_validation(logged_in_client, user, changes, field):
    response = post(logged_in_client, "password", password_payload(**changes))
    assert response.status_code == 400 and field in response.json()
    user.refresh_from_db()
    assert user.check_password(PASSWORD)


def test_change_password_requires_login(csrf_client):
    assert post(csrf_client, "password", password_payload()).status_code == 403


# --- address -------------------------------------------------------------------


def test_address_get_and_put(logged_in_client, user):
    address = {"address": "تهران", "zipcode": "1234567890", "street": "ولیعصر", "city": "تهران", "mobile": "09121234567"}
    assert logged_in_client.put(f"{BASE}/address/", address, format="json").status_code == 200
    assert logged_in_client.get(f"{BASE}/address/").json()["street"] == "ولیعصر"


def test_address_validation(logged_in_client):
    response = logged_in_client.put(
        f"{BASE}/address/", {"address": "x", "zipcode": "abc", "street": "x", "city": "x", "mobile": "1"}, format="json"
    )
    assert response.status_code == 400
    assert {"zipcode", "mobile"} <= set(response.json())


def test_address_requires_login(csrf_client):
    assert csrf_client.get(f"{BASE}/address/").status_code == 403
