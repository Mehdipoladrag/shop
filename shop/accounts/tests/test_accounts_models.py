from django.test import TestCase
from ..models import CustomUser, CustomProfileModel


class UserAccountModelTest(TestCase):
    """
    This is a test for user model
    we create a user and create a superuser
    """

    def test_create_user(self):
        self.user = CustomUser.objects.create_user(
            username="admin",
            email="admin@example.com",
            first_name="test f name",
            last_name="test l name",
            password="password",
        )
        user = CustomUser.objects.get(pk=self.user.pk)
        self.assertEqual(user.username, "admin")
        self.assertEqual(user.email, "admin@example.com")
        self.assertEqual(user.first_name, "test f name")
        self.assertEqual(user.last_name, "test l name")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        self.user = CustomUser.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            first_name="test f name",
            last_name="test l name",
            password="password",
        )
        user = CustomUser.objects.get(pk=self.user.pk)
        self.assertEqual(user.username, "admin")
        self.assertEqual(user.email, "admin@example.com")
        self.assertEqual(user.first_name, "test f name")
        self.assertEqual(user.last_name, "test l name")
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(isinstance(user, CustomUser))


class ProfileAccountTest(TestCase):
    """
    This is a test for ProfileModel And We Setup a User
    for use user in a profile section
    """

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="admin",
            email="admin@example.com",
            first_name="test f name",
            last_name="test l name",
            password="password",
        )

    def test_create_user_profile(self):
        self.card_number = "1234567890"
        self.profile = CustomProfileModel.objects.create(
            user=self.user,
            national_code="1234567890",
            address="enghelab",
            street="beheshti",
            city="tehran",
            mobile="09334223132",
            age=21,
            gender=False,
            card_number=self.card_number,
            iban="123456789",
            back_money=self.card_number,
            customer_image="test/",
            is_complete=True,
        )
        profile = CustomProfileModel.objects.get(pk=self.profile.pk)

        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.national_code, "1234567890")
        self.assertEqual(profile.address, "enghelab")
        self.assertEqual(profile.street, "beheshti")
        self.assertEqual(profile.city, "tehran")
        self.assertEqual(profile.mobile, "09334223132")
        self.assertEqual(profile.age, 21)
        self.assertEqual(profile.gender, False)
        self.assertEqual(profile.card_number, "1234567890")
        self.assertEqual(profile.back_money, self.profile.card_number)
        self.assertEqual(profile.iban, "123456789")
        self.assertEqual(profile.customer_image, "test/")
        self.assertTrue(profile.is_complete)

    def test_is_instance(self):
        self.test_create_user_profile()
        self.assertTrue(isinstance(self.profile, CustomProfileModel))
        self.assertTrue(isinstance(self.user, CustomUser))
