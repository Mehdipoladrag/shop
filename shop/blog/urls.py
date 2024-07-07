from django.urls import path, include
from blog.views import (
    BlogPageView, BlogDetailView,
    CategoryDetailView,
)

app_name = 'blog'

urlpatterns = [
    path('', BlogPageView.as_view(), name='bloglist1'),
    path('<slug:slug>/', BlogDetailView.as_view(), name='blogdetail1'),
    path('category/<slug:slug_cat>/', CategoryDetailView.as_view(), name='category_detail'),

    # API 
    path('api/v1/', include('blog.api.v1.urls')), 

]
