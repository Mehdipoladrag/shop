from django.test import TestCase
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework import status
from django.urls import reverse
from .serializers import ContactSerializer
from contact.models import Contact
from accounts.models import CustomUser
from django.utils import timezone

class ContactSerializerTestApi(TestCase):
    def test_serializer_valid_data(self): 
        data = {
            "name" : "mehdi", 
            "email" : "mehdi@gmail.com", 
            "phone" : "09353213243",
            "subject" : "TestSubject",
            "desc" : "TestDesc"
        }
        serializer = ContactSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['name'], 'mehdi')
        self.assertEqual(serializer.validated_data['email'], 'mehdi@gmail.com')
    
    def test_serializer_invalid_data(self): 
        data = {
            "email": "mehdi@gmail.com",
            "phone": "09353213243"
        }
        serializer = ContactSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
        self.assertIn('subject', serializer.errors)
        self.assertIn('desc', serializer.errors)
    
    def test_serializer_invalid_email(self):
        data = {
            "name": "mehdi",
            "email": "invalid-email",
            "phone": "09353213243",
            "subject": "TestSubject",
            "desc": "TestDesc"
        }
        serializer = ContactSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)



class ContactMethodTestApi(APITestCase):
    def setUp(self):

        self.admin_user = CustomUser.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='password'
        )
        
 
        self.token = RefreshToken.for_user(self.admin_user).access_token

 
        self.contact = Contact.objects.create(
            name="Admin Mehdi",
            email="mehdi@example.com",
            phone="09358321234",
            subject="Test Subject",
            desc="Test Description"
        )

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))

    def test_get_contact_list(self):
        url = reverse('contact:contact-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_contact_detail(self):
        url = reverse('contact:contact-detail', kwargs={'pk': self.contact.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Admin Mehdi')
        self.assertEqual(response.data['email'], 'mehdi@example.com')
        self.assertEqual(response.data['phone'], '09358321234')
        self.assertEqual(response.data['subject'], 'Test Subject')
        self.assertEqual(response.data['desc'], 'Test Description')

    def test_post_contact(self):
        url = reverse('contact:contact-list')
        data = {
            "name": "Test User",
            "email": "testuser@example.com",
            "phone": "1234567890",
            "subject": "Test Subject",
            "desc": "Test Description"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) 
        self.assertEqual(Contact.objects.count(), 2) 
        self.assertEqual(Contact.objects.latest('id').name, "Test User")

    def test_put_contact(self):
        """
          we can update an existing contact object.
        """
        url = reverse('contact:contact-detail', kwargs={'pk': self.contact.pk})
    
        data = {
            "name": "Updated Name",
            "email": "updatedemail@example.com",
            "phone": "0987654321",
            "subject": "Updated Subject",
            "desc": "Updated Description",
        }

        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.contact.refresh_from_db() 
        self.assertEqual(self.contact.name, "Updated Name")
        self.assertEqual(self.contact.email, "updatedemail@example.com")
        self.assertEqual(self.contact.phone, "0987654321")
        self.assertEqual(self.contact.subject, "Updated Subject")
        self.assertEqual(self.contact.desc, "Updated Description")

        
    def test_delete_contact(self): 
        url = reverse('contact:contact-detail', kwargs={'pk': self.contact.pk})

        response = self.client.delete(url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)  
        self.assertFalse(Contact.objects.filter(pk=self.contact.pk).exists())