from django.urls import path
from .views import (
  UserListApiView, UserProfileListApiView, 
)



urlpatterns = [
  path('users-list/', UserListApiView.as_view()),
  path('users-profile/', UserProfileListApiView.as_view()),


]
