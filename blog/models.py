from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _



class Category_blog(models.Model):
    name = models.CharField(max_length=100)
    slug_cat = models.SlugField(_("Slug"))
    def __str__(self):
        return self.name


class Blogs(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    blog_name = models.CharField(max_length=100)
    blog_image = models.ImageField(upload_to='blog_images/')
    category = models.ForeignKey(Category_blog, on_delete=models.CASCADE)
    blog_description = models.TextField()
    create_date = models.DateTimeField(_("Created At"), auto_now_add=True)
    update_date = models.DateTimeField(_("Update At"), auto_now=True)
    slug = models.SlugField(_("Slug"), unique=True)

    def __str__(self):
        return self.blog_name


class Visitor(models.Model):
    post = models.ForeignKey(Blogs, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Visitor: {self.blogs_details}"
