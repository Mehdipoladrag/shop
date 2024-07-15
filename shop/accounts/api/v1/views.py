# Libraries
from rest_framework import generics
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
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
    
    @swagger_auto_schema(
        operation_summary = "This is a endpoint for user list",
        operation_description="We Can See a user information and user list in this api",
        response = {
            200: openapi.Response(
                description="List of User",
                schema=UserSerializer(many=True),
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided."
            ),
            403: openapi.Response(description="Permission denied."),
        },
        tags=["User Information"]
    )
    def get(self, request):
        return self.list(request)


class UserProfileListApiView(generics.ListAPIView):
    """The job of this class is to return the list of users and profiles of each user"""

    queryset = CustomProfileModel.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary = "This is a endpoint for userprofile list",
        operation_description="We Can See a userprofile information and userprofile list in this api",
        response = {
            200: openapi.Response(
                description="List of UserProfile",
                schema=UserProfileSerializer(many=True),
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided."
            ),
            403: openapi.Response(description="Permission denied."),
        },
        tags=["Profile Information"]
    )
    def get(self, request): 
        return self.list(request)

# DELETE DATA API


class UserDeleteApiView(generics.DestroyAPIView):

    "Delete User API"

    queryset = CustomUser.objects.all()
    serializer_class = UserDataSerializer
    permission_classes = [AllowAny]
    lookup_field = "pk"


    @swagger_auto_schema(
        operation_summary = "This is a endpoint for Delete User",
        operation_description="Delete UserInformation in this api",
        response = {
            200: openapi.Response(
                description="Delete a UserProfile Information",
                schema=UserDataSerializer(),
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided."
            ),
            403: openapi.Response(description="Permission denied."),
        },
        tags=["User Information"]
    )

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class UserProfileDeleteApiView(generics.DestroyAPIView):

    "Delete Profile API"

    queryset = CustomProfileModel.objects.all()
    serializer_class = UserProfileDataSerializer
    lookup_field = "pk"
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary = "This is a endpoint for Delete UserProfile",
        operation_description="Delete UserProfile Information in this api",
        response = {
            200: openapi.Response(
                description="Delete a UserProfile Information",
                schema=UserProfileSerializer(),
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided."
            ),
            403: openapi.Response(description="Permission denied."),
        },
        tags=["Profile Information"]
    )

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
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

    @swagger_auto_schema(
        operation_summary = "This is a endpoint for Update User",
        operation_description="Update UserInformation in this api",
        response = {
            200: openapi.Response(
                description="Update User",
                schema=UserSerializer(),
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided."
            ),
            403: openapi.Response(description="Permission denied."),
        },
        tags=["User Information"]
    )

    def put(self,request,*args, **kwargs):
        return self.update(request,*args, **kwargs)
    

    @swagger_auto_schema(
        operation_summary = "This is a endpoint for Update User",
        operation_description="Update UserInformation in this api",
        response = {
            200: openapi.Response(
                description="Update User",
                schema=UserSerializer(),
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided."
            ),
            403: openapi.Response(description="Permission denied."),
        },
        tags=["User Information"]
    )

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

class UserProfileUpdateApiView(generics.UpdateAPIView):
    """
        A class to update where we can send
        our http request as Put or send a patch
    """

    queryset = CustomUser.objects.all()
    serializer_class = UserProfileDataSerializer
    permission_classes = [AllowAny]
    lookup_field = "pk"
    @swagger_auto_schema(
        operation_summary = "This is a endpoint for Update UserProfile Information",
        operation_description="We can Update UserProfile Information in this api",
        response = {
            200: openapi.Response(
                description="Update Profile User",
                schema=UserProfileSerializer(),
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided."
            ),
            403: openapi.Response(description="Permission denied."),
        },
        tags=["Profile Information"]
    )

    def put(self,request,*args, **kwargs):
        return self.update(request,*args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary = "This is a endpoint for Update UserProfile Information",
        operation_description="We can Update UserProfile Information in this api",
        response = {
            200: openapi.Response(
                description="Update Profile User",
                schema=UserProfileSerializer(),
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided."
            ),
            403: openapi.Response(description="Permission denied."),
        },
        tags=["Profile Information"]
    )

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

# CREATE DATA API


class UserCreateApiView(generics.CreateAPIView):
    """
    CreateUser Api
    """

    queryset = CustomUser.objects.all()
    serializer_class = UserDataSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary = "This is a endpoint for Create User",
        operation_description="Create User in this api",
        response = {
            200: openapi.Response(
                description="Create a New User",
                schema=UserSerializer(),
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided."
            ),
            403: openapi.Response(description="Permission denied."),
        },
        tags=["User Information"]
    )
    
    def post(self, request): 
        return self.create(request)
    
# DETAIL DATA API


class UserDetailApiView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = "pk"
    permission_classes = [AllowAny]


    @swagger_auto_schema(
        operation_summary = "This is a endpoint for user list",
        operation_description="We Can See a user information and user Detail with Pk in this api",
        response = {
            200: openapi.Response(
                description="Detail of User",
                schema=UserSerializer(),
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided."
            ),
            403: openapi.Response(description="Permission denied."),
        },
        tags=["User Information"]
    )

    def get(self, request, pk):
        return self.retrieve(request, pk)


class ProfileDetailApiView(generics.RetrieveAPIView):
    queryset = CustomProfileModel.objects.all()
    serializer_class = UserProfileDataSerializer
    lookup_field = "pk"
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary = "This is a endpoint for Profile Detail",
        operation_description="We Can See a user information and userProfile Detail in this api",
        response = {
            200: openapi.Response(
                description="Detail of UserProfile",
                schema=UserProfileSerializer(),
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided."
            ),
            403: openapi.Response(description="Permission denied."),
        },
        tags=["Profile Information"]
    )
    def get(self, request, pk):
        return self.retrieve(request, pk)