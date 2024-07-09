# Libraries
from rest_framework import generics
from rest_framework.permissions import AllowAny

# Modules
from accounts.models import CustomProfileModel, CustomUser
from .serializers import (
    UserSerializer,
    UserProfileSerializer,
    UserDataSerializer,
    UserProfileDataSerializer,
)

# View


# LIST DATA API


class UserListApiView(generics.ListAPIView):
    """The job of this class is to return the list of users"""

    queryset = CustomUser.objects.all().order_by("date_joined")
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserProfileListApiView(generics.ListAPIView):
    """The job of this class is to return the list of users and profiles of each user"""

    queryset = CustomProfileModel.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]


# DELETE DATA API


class UserDeleteApiView(generics.DestroyAPIView):

    "Delete User API"

    queryset = CustomUser.objects.all()
    serializer_class = UserDataSerializer
    permission_classes = [AllowAny]
    lookup_field = "pk"


class UserProfileDeleteApiView(generics.DestroyAPIView):

    "Delete Profile API"

    queryset = CustomProfileModel.objects.all()
    serializer_class = UserProfileDataSerializer
    lookup_field = "pk"
    permission_classes = [AllowAny]


# UPDATE DATA API


class UserUpdateApiView(generics.UpdateAPIView):
    """
    A class to update where we can send
    our http request as Put or send a patch
    """

    queryset = CustomUser.objects.all()
    serializer_class = UserDataSerializer
    permission_classes = [AllowAny]
    lookup_field = "pk"


class UserProfileUpdateApiView(generics.UpdateAPIView):
    """
    A class to update where we can send
    our http request as Put or send a patch
    """

    queryset = CustomUser.objects.all()
    serializer_class = UserProfileDataSerializer
    permission_classes = [AllowAny]
    lookup_field = "pk"


# CREATE DATA API


class UserCreateApiView(generics.CreateAPIView):
    """
    CreateUser Api
    """

    queryset = CustomUser.objects.all()
    serializer_class = UserDataSerializer
    permission_classes = [AllowAny]


# DETAIL DATA API


class UserDetailApiView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = "pk"
    permission_classes = [AllowAny]


class ProfileDetailApiView(generics.RetrieveAPIView):
    queryset = CustomProfileModel.objects.all()
    serializer_class = UserProfileDataSerializer
    lookup_field = "pk"
    permission_classes = [AllowAny]
