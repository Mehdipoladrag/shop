from django.test import TestCase
from django.urls import reverse
from ..models import Blogs, Category_blog
from accounts.models import CustomUser


class BlogPageViewTest(TestCase):
    def setUp(self):

        self.user = CustomUser.objects.create_user(
            username="testuser", password="12345"
        )

        self.category = Category_blog.objects.create(
            name="Test Category", slug_cat="test-category"
        )

        for i in range(3):
            Blogs.objects.create(
                username=self.user,
                blog_name=f"Test Blog {i}",
                blog_image="path/to/image.jpg",
                category=self.category,
                blog_description="This is a test blog.",
                slug=f"test-blog-{i}",
            )

    def test_blog_page_view_status_code(self):
        url = reverse("blog:bloglist1")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class CategoryDetailViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser", password="12345"
        )
        self.category = Category_blog.objects.create(
            name="Test Category", slug_cat="test-category"
        )
        self.blog = Blogs.objects.create(
            username=self.user,
            blog_name="Test Blog",
            blog_image="path/to/image.jpg",
            category=self.category,
            blog_description="This is a test blog.",
            slug="test-blog",
        )

    def test_category_creation(self):
        category = Category_blog.objects.get(name="Test Category")
        self.assertEqual(category.slug_cat, "test-category")

    def test_blog_creation(self):
        blog = Blogs.objects.get(blog_name="Test Blog")
        self.assertEqual(blog.username, self.user)
        self.assertEqual(blog.category, self.category)
        self.assertEqual(blog.slug, "test-blog")
