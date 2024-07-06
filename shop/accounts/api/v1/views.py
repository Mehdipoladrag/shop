# Libraries
from django.http import HttpResponse
from django.views import View
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

# Modules 
from accounts.models import CustomProfileModel, CustomUser
from .serializers import UserSerializer, UserProfileSerializer 

# View





class UserListApiView(generics.ListAPIView): 

  """ The job of this class is to return the list of users """

  queryset = CustomUser.objects.all().order_by('date_joined')
  serializer_class = UserSerializer
  permission_classes = [AllowAny]
  

class UserProfileListApiView(generics.ListAPIView): 

  """ The job of this class is to return the list of users and profiles of each user """
  
  queryset = CustomProfileModel.objects.all()
  serializer_class = UserProfileSerializer
  permission_classes = [AllowAny] 

