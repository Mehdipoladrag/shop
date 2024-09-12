# Libraries
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser
from drf_yasg.utils import swagger_auto_schema  # type: ignore
from drf_yasg import openapi  # type: ignore
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator

# Modules
from .filters.user_join_filter import (
    UserProfileSearchFilter,
    UserOrderFilter,
    UserSearchFilter,
)
from .filters.max_user_order_filter import UserMaxOrderFilter
from accounts.models import CustomProfileModel, CustomUser
from .serializers import (
    UserSerializer,
    UserProfileSerializer,
    UserDataSerializer,
    UserProfileDataSerializer,
    CustomTokenObtainPairSerializer,
    UserOrderSerializer,
    UserCompleteSerializer,
)
from shop.models import Order

# View


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class LoginApiView(APIView):
    """Login API View For authentication To a Panel Admin"""

    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Login endpoint for obtaining tokens",
        operation_description="Authenticate user and obtain tokens.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "username": openapi.Schema(
                    type=openapi.TYPE_STRING, description="The username of the user"
                ),
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING, description="The password of the user"
                ),
            },
            required=["username", "password"],
        ),
        responses={
            200: openapi.Response(
                description="Login successful, token returned.",
                schema=CustomTokenObtainPairSerializer(),
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided."
            ),
            403: openapi.Response(description="Permission denied."),
        },
        tags=["Authentication"],
    )
    def post(self, request, *args, **kwargs):
        serializer = CustomTokenObtainPairSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


# LIST DATA API


@method_decorator(never_cache, name="dispatch")
class UserListApiView(generics.ListAPIView):
    """The job of this class is to return the list of users"""

    queryset = CustomUser.objects.select_related().order_by("date_joined")
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [UserOrderFilter, UserSearchFilter]


@method_decorator(never_cache, name="dispatch")
class UserProfileListApiView(generics.ListAPIView):
    """The job of this class is to return the list of users and profiles of each user"""

    queryset = CustomProfileModel.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [UserProfileSearchFilter]


# DELETE DATA API


class UserDeleteApiView(generics.DestroyAPIView):

    "Delete User API"

    queryset = CustomUser.objects.all()
    serializer_class = UserDataSerializer
    permission_classes = [IsAdminUser]
    lookup_field = "pk"

    @swagger_auto_schema(
        operation_summary="This is a endpoint for Delete User",
        operation_description="Delete UserInformation in this api",
        response={
            200: openapi.Response(
                description="Delete a UserProfile Information",
                schema=UserDataSerializer(),
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided."
            ),
            403: openapi.Response(description="Permission denied."),
        },
        tags=["User Information"],
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request)


class UserProfileDeleteApiView(generics.DestroyAPIView):

    "Delete Profile API"

    queryset = CustomProfileModel.objects.all()
    serializer_class = UserProfileDataSerializer
    lookup_field = "pk"
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="This is a endpoint for Delete UserProfile",
        operation_description="Delete UserProfile Information in this api",
        response={
            200: openapi.Response(
                description="Delete a UserProfile Information",
                schema=UserProfileSerializer(),
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided."
            ),
            403: openapi.Response(description="Permission denied."),
        },
        tags=["Profile Information"],
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
    permission_classes = [IsAdminUser]
    lookup_field = "pk"

    @swagger_auto_schema(
        operation_summary="This is a endpoint for Update User",
        operation_description="Update UserInformation in this api",
        response={
            200: openapi.Response(
                description="Update User",
                schema=UserSerializer(),
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided."
            ),
            403: openapi.Response(description="Permission denied."),
        },
        tags=["User Information"],
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="This is a endpoint for Update User",
        operation_description="Update UserInformation in this api",
        response={
            200: openapi.Response(
                description="Update User",
                schema=UserSerializer(),
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided."
            ),
            403: openapi.Response(description="Permission denied."),
        },
        tags=["User Information"],
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
    permission_classes = [IsAdminUser]
    lookup_field = "pk"

    @swagger_auto_schema(
        operation_summary="This is a endpoint for Update UserProfile Information",
        operation_description="We can Update UserProfile Information in this api",
        response={
            200: openapi.Response(
                description="Update Profile User",
                schema=UserProfileSerializer(),
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided."
            ),
            403: openapi.Response(description="Permission denied."),
        },
        tags=["Profile Information"],
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="This is a endpoint for Update UserProfile Information",
        operation_description="We can Update UserProfile Information in this api",
        response={
            200: openapi.Response(
                description="Update Profile User",
                schema=UserProfileSerializer(),
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided."
            ),
            403: openapi.Response(description="Permission denied."),
        },
        tags=["Profile Information"],
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
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="This is a endpoint for Create User",
        operation_description="Create User in this api",
        response={
            200: openapi.Response(
                description="Create a New User",
                schema=UserSerializer(),
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided."
            ),
            403: openapi.Response(description="Permission denied."),
        },
        tags=["User Information"],
    )
    def post(self, request):
        return self.create(request)


# DETAIL DATA API


class UserDetailApiView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = "pk"
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="This is a endpoint for user list",
        operation_description="We Can See a user information and user Detail with Pk in this api",
        response={
            200: openapi.Response(
                description="Detail of User",
                schema=UserSerializer(),
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided."
            ),
            403: openapi.Response(description="Permission denied."),
        },
        tags=["User Information"],
    )
    def get(self, request, pk):
        return self.retrieve(request, pk)


class ProfileDetailApiView(generics.RetrieveAPIView):
    queryset = CustomProfileModel.objects.all()
    serializer_class = UserProfileDataSerializer
    lookup_field = "pk"
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="This is a endpoint for Profile Detail",
        operation_description="We Can See a user information and userProfile Detail in this api",
        response={
            200: openapi.Response(
                description="Detail of UserProfile",
                schema=UserProfileSerializer(),
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided."
            ),
            403: openapi.Response(description="Permission denied."),
        },
        tags=["Profile Information"],
    )
    def get(self, request, pk):
        return self.retrieve(request, pk)


class UserOrderFilterApiView(generics.ListAPIView):
    queryset = Order.objects.select_related("customer").all()
    serializer_class = UserOrderSerializer
    filter_backends = [UserMaxOrderFilter]
    permission_classes = [IsAdminUser]


@method_decorator(never_cache, name="dispatch")
class UserIsCompleteApiView(generics.ListAPIView):
    serializer_class = UserCompleteSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return CustomProfileModel.objects.filter(is_complete=True).order_by(
            "-user__date_joined"
        )
