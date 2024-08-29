from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class JWTAuthTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(
            username='testuser',
            email='testuser@example.com',
            password='password'
        )


        self.token_obtain_url = reverse('accounts:login-api')
        self.token_refresh_url = reverse('token_refresh')
        self.token_verify_url = reverse('token_verify')
        response = self.client.post(self.token_obtain_url, {
            'username': 'testuser',
            'password': 'password'
        }, format='json')
        
        self.access_token = response.data['access']
        self.refresh_token = response.data['refresh']

    def test_obtain_token(self):

        data = {
            'username': 'testuser',
            'password': 'password'
        }

        response = self.client.post(self.token_obtain_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_refresh_token(self):
        refresh = RefreshToken.for_user(self.user)
        data = {
            'refresh': str(refresh)
        }


        response = self.client.post(self.token_refresh_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_invalid_token(self):
        data = {
            'refresh': 'invalid_token'
        }

        response = self.client.post(self.token_refresh_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_verify_access_token(self):
        data = { 
            'token': str(self.access_token)
        }
        
        response = self.client.post(self.token_verify_url, data, format='json')


        self.assertEqual(response.status_code, status.HTTP_200_OK)
