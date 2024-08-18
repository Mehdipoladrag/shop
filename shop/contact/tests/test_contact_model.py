from django.test import TestCase
from contact.models import Contact

# Create your tests here.


class ContactModelTest(TestCase):
    """
    Test Contact Model With TestCase &
    Create a Valid Data
    """

    def test_create_message(self):
        self.contact = Contact.objects.create(
            name="mehdi",
            email="mehdiPoladrag@gmail.com",
            phone="09351234321",
            subject="Test Subject",
            desc="Test Description",
        )

        retrieved_contact = Contact.objects.get(id=self.contact.id)

        self.assertEqual(retrieved_contact.name, "mehdi")
        self.assertEqual(retrieved_contact.email, "mehdiPoladrag@gmail.com")
        self.assertEqual(retrieved_contact.phone, "09351234321")
        self.assertEqual(retrieved_contact.subject, "Test Subject")
        self.assertEqual(retrieved_contact.desc, "Test Description")

        self.assertEqual(Contact.objects.count(), 1)
