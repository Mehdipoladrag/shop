from django.test import TestCase
from ..forms import ContactUsForm

# Create your tests here.


class ContactFormTest(TestCase):
    """
    We Need To Use a Persian Subject and Message
    Because We Validate Form with a
    Persian Words In Forms.
    """

    def test_form_with_valid_data(self):
        form = ContactUsForm(
            data={
                "name": "Admin Mehdi",
                "email": "mehdi@gmail.com",
                "phone": "09354323212",
                "subject": "موضوع تست",
                "desc": "پیام تست",
            }
        )
        self.assertTrue(form.is_valid())

    def test_from_with_no_data(self):
        form = ContactUsForm(data={})
        self.assertFalse(form.is_valid())

    def test_form_with_invalid_data(self):
        form = ContactUsForm(
            data={
                "name": "Admin Mehdi",
                "email": "mehdigmail.com",
                "phone": "09354323212",
                "subject": "موضوع تست",
                "desc": "پیام تست",
            }
        )
        email_errors = form.errors.get("email", [])
        self.assertIn("Enter a valid email address.", email_errors)
        self.assertIn("لطفا ایمیل را به درستی وارد کنید", email_errors)
