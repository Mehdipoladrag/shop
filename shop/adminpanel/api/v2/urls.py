from django.urls import path 
from .views import CateApi


urlpatterns = [
    path('categories/', CateApi.as_view()),
]
