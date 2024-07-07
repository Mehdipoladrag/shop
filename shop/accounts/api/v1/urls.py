from django.urls import path
from .views import (
  UserListApiView, UserProfileListApiView, 
  UserUpdateApiView, UserCreateApiView,
  UserDeleteApiView, UserProfileDeleteApiView,
  UserProfileUpdateApiView, 
)



urlpatterns = [
  # List
  path('users-list/', UserListApiView.as_view()),
  path('users-profile/', UserProfileListApiView.as_view()),

  # Update 
  path('users-change-info/<int:pk>/', UserUpdateApiView.as_view()),
  path('users-change-profile/<int:pk>/', UserProfileUpdateApiView.as_view()),

  # Create 
  path('users-create/', UserCreateApiView.as_view()),

  # Delete 
  path('users-delete/<int:pk>/', UserDeleteApiView.as_view()),
  path('users-profile-delete/<int:pk>/', UserProfileDeleteApiView.as_view()),
]
