from django.test import TestCase, SimpleTestCase
from contact.models import Contact
from django.urls import reverse, resolve
from .views import ContactPageView
# Create your tests here.

class ContactModelTest(TestCase):
    def test_create_message(self):
        # Create a new Contact object
        self.contact = Contact.objects.create(
            name="mehdi",
            email="mehdiPoladrag@gmail.com",
            phone="09351234321",
            subject="Test Subject",
            desc="Test Description"
        )
        
        retrieved_contact = Contact.objects.get(id=self.contact.id)

        self.assertEqual(retrieved_contact.name, "mehdi")
        self.assertEqual(retrieved_contact.email, "mehdiPoladrag@gmail.com")
        self.assertEqual(retrieved_contact.phone, "09351234321")
        self.assertEqual(retrieved_contact.subject, "Test Subject")
        self.assertEqual(retrieved_contact.desc, "Test Description")

        self.assertEqual(Contact.objects.count(), 1)


class UrlTest(SimpleTestCase):
    """
        SimpleTestCase It is given for tests without a database
    """
    def test_contact_url_reslove(self):
        url = reverse("contact:contact1")
        self.assertEqual(
            resolve(url).func.view_class, ContactPageView
        )