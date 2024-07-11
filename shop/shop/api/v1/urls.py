from django.urls import path
from .views import (
    CategoryGetApiView,
    CategoryPutDeleteApiView,
    CategoryCreateAPIView,
    CategoryDetailApiView,
)


urlpatterns = [
    path("category-list/", CategoryGetApiView.as_view()),
    path("category-create/", CategoryCreateAPIView.as_view()),
    path("category-detail/<pk>/", CategoryDetailApiView.as_view()),
    path("category-data/<pk>/", CategoryPutDeleteApiView.as_view()),
]
