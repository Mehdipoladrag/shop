from django.urls import path
from blog.views import (
    blog_page, blog_detail,
    categor_detail,
)

app_name = 'blog'

urlpatterns = [
    path('', blog_page, name='bloglist1'),
    path('<slug:slug>/', blog_detail, name='blogdetail1'),
    path('category/<str:slug_cat>/', categor_detail, name='category_detail'),

]
