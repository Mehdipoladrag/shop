from django.urls import path
from .views import (
  UserListApiView, UserProfileListApiView, 
  UserUpdateApiView, UserCreateApiView,
  UserDeleteApiView, 
)



urlpatterns = [
  # List
  path('users-list/', UserListApiView.as_view()),
  path('users-profile/', UserProfileListApiView.as_view()),

  # Update 
  path('users-change-profile/<int:pk>/', UserUpdateApiView.as_view()),

  # Create 
  path('users-create/', UserCreateApiView.as_view()),

  # Delete 
  path('users-delete/<int:pk>/', UserDeleteApiView.as_view()),
]
