from django.test import TestCase
from ..models import CustomUser

class UserAccountModelTest(TestCase):
    def test_create_user(self): 
        self.user = CustomUser.objects.create_user(
            username= 'admin',
            email='admin@example.com',
            first_name = 'test f name',
            last_name = 'test l name',
            password= 'password'
            
        )
        user = CustomUser.objects.get(pk=self.user.pk)
        self.assertEqual(user.username , 'admin')
        self.assertEqual(user.email, 'admin@example.com')
        self.assertEqual(user.first_name, 'test f name')
        self.assertEqual(user.last_name, 'test l name')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
    def test_create_superuser(self):
        self.user = CustomUser.objects.create_superuser(
            username= 'admin',
            email='admin@example.com',
            first_name = 'test f name',
            last_name = 'test l name',
            password= 'password'
        )
        user = CustomUser.objects.get(pk=self.user.pk)
        self.assertEqual(user.username , 'admin')
        self.assertEqual(user.email, 'admin@example.com')
        self.assertEqual(user.first_name, 'test f name')
        self.assertEqual(user.last_name, 'test l name')
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)