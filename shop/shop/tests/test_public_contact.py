import pytest
from rest_framework.test import APIClient

from contact.models import Contact

pytestmark = pytest.mark.django_db

URL = "/shop/api/v1/public/contact/"
MESSAGE = {"name": "علی", "email": "ali@example.com", "phone": "09121234567", "subject": "سلام", "desc": "پیام"}


def test_valid_message_is_stored():
    assert APIClient().post(URL, MESSAGE, format="json").status_code == 201
    assert Contact.objects.get().phone == "09121234567"


def test_persian_digits_in_the_phone_are_normalized():
    APIClient().post(URL, {**MESSAGE, "phone": "۰۹۱۲۱۲۳۴۵۶۷"}, format="json")
    assert Contact.objects.get().phone == "09121234567"


@pytest.mark.parametrize("phone", ["not a phone", "123", "0912123456", "091212345678", "08121234567"])
def test_invalid_phones_are_rejected(phone):
    response = APIClient().post(URL, {**MESSAGE, "phone": phone}, format="json")
    assert response.status_code == 400 and "phone" in response.json()
    assert not Contact.objects.exists()


def test_the_form_is_rate_limited():
    client = APIClient()
    statuses = [client.post(URL, MESSAGE, format="json").status_code for _ in range(12)]
    assert 429 in statuses[10:]
