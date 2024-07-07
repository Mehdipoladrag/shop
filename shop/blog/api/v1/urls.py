from django.urls import path 
from .views import (
  BlogDetailmixin, BloglistMixin
)

urlpatterns = [
  # Blogs
  path('blog-list/', BloglistMixin.as_view()),
  path('blog-detail/<pk>/', BlogDetailmixin.as_view()),

  # Categories

  # Visitors 

]
