from django.contrib import admin
from blog.models import Category_blog, Blogs, Visitor
# Register your models here.

admin.site.register(Category_blog)
admin.site.register(Blogs)
admin.site.register(Visitor)
