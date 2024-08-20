import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import CustomUser
from ..models import Category_blog, Blogs
from rest_framework import status
from django.utils import timezone
from rest_framework.test import RequestsClient


@pytest.mark.django_db
class TestBlogApiUrl:
    def setup_method(self):
        self.is_admin = CustomUser.objects.create_superuser(
            username='test',
            email='test@example.com',
            password='test'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.is_admin)
        
        self.category = Category_blog.objects.create(name="BlogTestCategory", slug_cat="test-category")
        self.blog = Blogs.objects.create(
            username=self.is_admin,
            blog_name="Test Blog",
            blog_image="test_image.png",
            category=self.category,
            blog_description="This is a test blog.",
            slug="test-blog"
        )

    def test_get_blog_response_200(self):
        url = reverse('blog:api-v1:api-blog-list')  
        response = self.client.get(url)
        assert response.status_code == 200
 

    def test_get_detail_blog_response_200(self): 
        url = reverse('blog:api-v1:api-blog-detail', kwargs={'pk': self.blog.id})
        response = self.client.get(url)
        assert response.status_code == 200
