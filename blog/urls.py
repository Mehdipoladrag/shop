from django.urls import path
from blog.views import (
    blog_page, blog_detail,
    categor_detail,
    ##
    BloglistMixin, BlogDetailmixin,
    CategoryBlogListmixin, CategoryBlogDetailmixin,
    VisitorBlogListmixin, VisitorBlogDetailmixin,
)

app_name = 'blog'

urlpatterns = [
    path('', blog_page, name='bloglist1'),
    path('<slug:slug>/', blog_detail, name='blogdetail1'),
    path('category/<str:slug_cat>/', categor_detail, name='category_detail'),
    path('api/blog-list/', BloglistMixin.as_view()),
    path('api/blog-detail/<pk>/', BlogDetailmixin.as_view()),
    path('api/category-list/', CategoryBlogListmixin.as_view()),
    path('api/category-detail/<pk>/', CategoryBlogDetailmixin.as_view()),
    path('api/Visitor-list/', VisitorBlogListmixin.as_view()),
    path('api/Visitor-detail/<pk>/', VisitorBlogDetailmixin.as_view()),
]
