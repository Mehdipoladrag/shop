from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _



class Category_blog(models.Model):
    name = models.CharField(_("نام دسته بندی"),max_length=100)
    slug_cat = models.SlugField(_("یو ار ال دسته بندی"))
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'دسته بندی وبلاگ'
        verbose_name_plural  = 'دسته بندی وبلاگ ها'

class Blogs(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='نام کاربری')
    blog_name = models.CharField(_("نام وبلاگ"),max_length=100)
    blog_image = models.ImageField(_("عکس وبلاگ"),upload_to='blog_images/')
    category = models.ForeignKey(Category_blog, on_delete=models.CASCADE, verbose_name='دسته بندی وبلاگ')
    blog_description = models.TextField(_("توضیحات وبلاگ"),)
    create_date = models.DateTimeField(_("زمان ساخت وبلاگ"), auto_now_add=True)
    update_date = models.DateTimeField(_("زمان ویرایش وبلاگ"), auto_now=True)
    slug = models.SlugField(_("یو ار ال وبلاگ"), unique=True)

    def __str__(self):
        return self.blog_name
    class Meta:
        verbose_name = 'وبلاگ'
        verbose_name_plural  = 'وبلاگ ها'

class Visitor(models.Model):
    post = models.ForeignKey(Blogs, on_delete=models.CASCADE,verbose_name='وبلاگ')
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='نشر دهنده توسط')
    timestamp = models.DateTimeField(_("تاریخ ساخت"),auto_now_add=True)

    def __str__(self):
        return f"Visitor: {self.blogs_details}"
    class Meta:
        verbose_name = 'بازدید کننده '
        verbose_name_plural  = 'بازدید کنندگان'