from django.test import TestCase
from contact.api.v1.serializers import ContactSerializer


class ContactSerializerTestApi(TestCase):
    """
    Test Serializer
    """

    def test_serializer_valid_data(self):
        data = {
            "name": "mehdi",
            "email": "mehdi@gmail.com",
            "phone": "09353213243",
            "subject": "TestSubject",
            "desc": "TestDesc",
        }
        serializer = ContactSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["name"], "mehdi")
        self.assertEqual(serializer.validated_data["email"], "mehdi@gmail.com")

    def test_serializer_invalid_data(self):
        data = {"email": "mehdi@gmail.com", "phone": "09353213243"}
        serializer = ContactSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)
        self.assertIn("subject", serializer.errors)
        self.assertIn("desc", serializer.errors)

    def test_serializer_invalid_email(self):
        data = {
            "name": "mehdi",
            "email": "invalid-email",
            "phone": "09353213243",
            "subject": "TestSubject",
            "desc": "TestDesc",
        }
        serializer = ContactSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)
