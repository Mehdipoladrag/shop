from django.test import TestCase
from django.urls import reverse
from ..forms import ContactUsForm
from django.contrib.messages import get_messages

# Create your tests here.


class ContactViewTest(TestCase):
    """
    Test View For Send a Message From View
    with Valid Data Or Invalid Data
    """

    def test_contact_get_view(self):
        response = self.client.get(reverse("contact:contact1"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "contact/contactpage.html")

        self.assertIn("form", response.context)

        self.assertIsInstance(response.context["form"], ContactUsForm)

    def test_contact_post_data_view(self):
        response = self.client.post(
            reverse("contact:contact1"),
            {
                "name": "mehdi",
                "email": "mehdi@gmail.com",
                "phone": "09354323212",
                "subject": "TestSubject",
                "desc": "TestDesc",
            },
        )
        self.assertEqual(response.status_code, 302)
        messages_list = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(str(messages_list[0]), "با موفقیت ارسال شد")
        self.assertRedirects(response, reverse("home:home1"))

    def test_contact_view_with_invalid_data(self):
        response = self.client.post(
            reverse("contact:contact1"),
            {
                "name": "Admin Mehdi",
                "email": "mehdigmail.com",
                "phone": "09354323212",
                "subject": "موضوع تست",
                "desc": "پیام تست",
            },
        )

        self.assertEqual(response.status_code, 200)

        messages_list = list(response.context["messages"])
        self.assertEqual(len(messages_list), 1)
        self.assertIn(
            "مشکلی در ارسال پیام شما به وجود آمده است", str(messages_list[0].message)
        )
