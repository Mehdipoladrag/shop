from django.urls import path
from .views import (
    BloglistMixinView,
    BlogDetailmixinView,
    CategoryBlogListmixinView,
    CategoryBlogDetailmixinView,
    VisitorBlogDetailmixinView,
    VisitorBlogListmixinView,
)

app_name = "api-v1"

urlpatterns = [
    # Blogs
    path("blog-list/", BloglistMixinView.as_view(), name="api-blog-list"),
    path("blog-detail/<pk>/", BlogDetailmixinView.as_view(), name="api-blog-detail"),
    # Categories
    path("category-list/", CategoryBlogListmixinView.as_view()),
    path("category-detail/<pk>/", CategoryBlogDetailmixinView.as_view()),
    # Visitors
    path("Visitor-list/", VisitorBlogListmixinView.as_view()),
    path("Visitor-detail/<pk>/", VisitorBlogDetailmixinView.as_view()),
]
