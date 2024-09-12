from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import BlogPageView, BlogDetailView, CategoryDetailView


class BlogUrlsTest(SimpleTestCase):
    """
    Test All Url For Blog App
    """

    def test_blog_list_url_reslove(self):
        url = reverse("blog:bloglist1")
        self.assertEqual(resolve(url).func.view_class, BlogPageView)

    def test_blog_detail_url_reslove(self):
        url = reverse("blog:blogdetail1", kwargs={"slug": 1})
        self.assertEqual(resolve(url).func.view_class, BlogDetailView)

    def test_category_detail_url_reslove(self):
        url = reverse("blog:category_detail", kwargs={"slug_cat": 1})
        self.assertEqual(resolve(url).func.view_class, CategoryDetailView)
