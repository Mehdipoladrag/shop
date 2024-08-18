from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import ContactPageView

# Create your tests here.


class UrlTest(SimpleTestCase):
    """
    SimpleTestCase It is given for tests without a database
    """

    def test_contact_url_reslove(self):
        url = reverse("contact:contact1")
        self.assertEqual(resolve(url).func.view_class, ContactPageView)
