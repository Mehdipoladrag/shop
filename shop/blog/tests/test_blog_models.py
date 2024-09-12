from django.test import TestCase
from blog.models import Blogs, Category_blog, Visitor
from django.utils import timezone
from accounts.models import CustomUser


class BlogModelTest(TestCase):
    def setUp(self):
        self.admin_user = CustomUser.objects.create_superuser(
            username="admin", email="admin@example.com", password="password"
        )
        self.category = Category_blog.objects.create(
            name="BlogTestcategory", slug_cat="Test"
        )

    def test_create_blog(self):

        self.blog = Blogs.objects.create(
            username=self.admin_user,
            blog_name="Test Blogname",
            blog_image="test/",
            category=self.category,
            blog_description="test Desc",
            slug="test",
            create_date=timezone.now(),
        )

        blog = Blogs.objects.get(pk=self.blog.pk)

        self.assertEqual(blog.username, self.admin_user)
        self.assertEqual(blog.blog_name, "Test Blogname")
        self.assertEqual(blog.blog_image, "test/")
        self.assertEqual(blog.category, self.category)
        self.assertEqual(blog.blog_description, "test Desc")
        self.assertEqual(blog.slug, "test")
        self.assertIsNotNone(blog.create_date)
        self.assertIsNotNone(blog.update_date)


class BlogCategoryModelTest(TestCase):
    def setUp(self):
        self.blogcategory = Category_blog.objects.create(
            name="BlogTestcategory", slug_cat="Test"
        )

    def test_create_blog_category(self):
        blog = Category_blog.objects.get(pk=self.blogcategory.pk)

        self.assertEqual(blog.name, "BlogTestcategory")
        self.assertEqual(blog.slug_cat, "Test")

    def test_blog_category_name_max_length(self):
        max_length = Category_blog._meta.get_field("name").max_length
        self.assertEqual(max_length, 100)


class VisitorModelTest(TestCase):
    def setUp(self):

        self.admin_user = CustomUser.objects.create_superuser(
            username="admin", email="admin@example.com", password="password"
        )

        self.category = Category_blog.objects.create(
            name="Test Category", slug_cat="test-category"
        )

        self.blog = Blogs.objects.create(
            username=self.admin_user,
            blog_name="Test Blogname",
            blog_image="test/",
            category=self.category,
            blog_description="test Desc",
            slug="test",
            create_date=timezone.now(),
        )

    def test_create_visitor(self):
        self.visitor = Visitor.objects.create(
            post=self.blog, user=self.admin_user, timestamp=timezone.now()
        )

        visitor = Visitor.objects.get(pk=self.visitor.pk)

        self.assertEqual(visitor.post, self.blog)
        self.assertEqual(visitor.user, self.admin_user)
        self.assertAlmostEqual(
            visitor.timestamp, timezone.now(), delta=timezone.timedelta(seconds=1)
        )
