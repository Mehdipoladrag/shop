from django.urls import path
from .views import (
    # Category
    CategoryGetApiView,
    CategoryPutDeleteApiView,
    CategoryCreateAPIView,
    CategoryDetailApiView,
    # Brand
    BrandGetApiView, 
    BrandCreateApiView, 
    BrandDetailApiView,
    BrandPutDeleteApiView,
)


urlpatterns = [
    # Category Api Route 
    path("category-list/", CategoryGetApiView.as_view()),
    path("category-create/", CategoryCreateAPIView.as_view()),
    path("category-detail/<pk>/", CategoryDetailApiView.as_view()),
    path("category-data/<pk>/", CategoryPutDeleteApiView.as_view()),
    # Brand Api Route
    path("brand-list/", BrandGetApiView.as_view()),
    path("brand-create/", BrandCreateApiView.as_view()),
    path("brand-detail/<pk>/", BrandDetailApiView.as_view()),
    path("brand-data/<pk>/", BrandPutDeleteApiView.as_view()),

]
