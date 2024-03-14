from django.urls import path
from blog.views import (
    BlogPage, BlogDetail,
    CategoryDetail,
    ##
    BloglistMixin, BlogDetailmixin,
    CategoryBlogListmixin, CategoryBlogDetailmixin,
    VisitorBlogListmixin, VisitorBlogDetailmixin,
)

app_name = 'blog'

urlpatterns = [
    path('', BlogPage.as_view(), name='bloglist1'),
    path('<slug:slug>/', BlogDetail.as_view(), name='blogdetail1'),
    path('category/<slug:slug_cat>/', CategoryDetail.as_view(), name='category_detail'),
    path('api/blog-list/', BloglistMixin.as_view()),
    path('api/blog-detail/<pk>/', BlogDetailmixin.as_view()),
    path('api/category-list/', CategoryBlogListmixin.as_view()),
    path('api/category-detail/<pk>/', CategoryBlogDetailmixin.as_view()),
    path('api/Visitor-list/', VisitorBlogListmixin.as_view()),
    path('api/Visitor-detail/<pk>/', VisitorBlogDetailmixin.as_view()),
]
