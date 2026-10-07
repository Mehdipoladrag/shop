from django.contrib.auth import login, logout, update_session_auth_hash
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView

from accounts.models import CustomProfileModel
from shop.api.v1.public_serializers import OrderSerializer
from shop.models import Order
from shopproject.security import CsrfProtectedMixin

from .customer_serializers import (
    AddressSerializer,
    ChangePasswordSerializer,
    LoginSerializer,
    ProfileSerializer,
    RegisterSerializer,
)

TAG = ["Customer"]


class LoginThrottle(AnonRateThrottle):
    """Slows down password guessing."""

    scope = "customer_login"
    rate = "10/min"


class RegisterThrottle(AnonRateThrottle):
    scope = "customer_register"
    rate = "10/hour"


class CustomerApiView(APIView):
    """Base of the customer endpoints: session login, CSRF checked on every change."""

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]


def session_payload(user):
    """What the frontend needs to know about the logged in user."""
    profile = CustomProfileModel.objects.filter(user=user).first()
    return {
        "is_authenticated": True,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "is_staff": user.is_staff,
        "profile_complete": bool(profile and profile.is_complete),
    }


def get_profile(user):
    """The profile of a user, created on first use (admins have none)."""
    profile, _ = CustomProfileModel.objects.get_or_create(user=user)
    return profile


class CsrfCookieApiView(APIView):
    """Sets the `csrftoken` cookie that the frontend echoes in `X-CSRFToken`."""

    authentication_classes = []
    permission_classes = [AllowAny]

    @swagger_auto_schema(tags=TAG)
    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        return Response({"detail": "ok"})


class RegisterApiView(CsrfProtectedMixin, APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = [RegisterThrottle]

    @swagger_auto_schema(tags=TAG, request_body=RegisterSerializer)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"username": user.username}, status=status.HTTP_201_CREATED)


class LoginApiView(CsrfProtectedMixin, APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = [LoginThrottle]

    @swagger_auto_schema(tags=TAG, request_body=LoginSerializer)
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        get_profile(user)
        return Response(session_payload(user))


class LogoutApiView(CsrfProtectedMixin, APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    @swagger_auto_schema(tags=TAG)
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileApiView(CustomerApiView):
    """Profile of the logged in user; changes are partial and may include a picture."""

    parser_classes = [JSONParser, MultiPartParser, FormParser]

    @swagger_auto_schema(tags=TAG, responses={200: ProfileSerializer()})
    def get(self, request):
        serializer = ProfileSerializer(get_profile(request.user), context={"request": request})
        return Response(serializer.data)

    @swagger_auto_schema(tags=TAG, request_body=ProfileSerializer)
    def patch(self, request):
        serializer = ProfileSerializer(
            get_profile(request.user), data=request.data, partial=True, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ChangePasswordApiView(CustomerApiView):
    @swagger_auto_schema(tags=TAG, request_body=ChangePasswordSerializer)
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # Changing the password invalidates sessions; keep the current one.
        update_session_auth_hash(request, user)
        return Response({"detail": "رمز عبور با موفقیت تغییر کرد."})


class AddressApiView(CustomerApiView):
    @swagger_auto_schema(tags=TAG, responses={200: AddressSerializer()})
    def get(self, request):
        return Response(AddressSerializer(get_profile(request.user)).data)

    @swagger_auto_schema(tags=TAG, request_body=AddressSerializer)
    def put(self, request):
        serializer = AddressSerializer(get_profile(request.user), data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class OrderPagination(PageNumberPagination):
    page_size = 10


def customer_orders(user):
    """Orders of one customer, newest first; every query is limited to that customer."""
    return (
        Order.objects.filter(customer=user)
        .prefetch_related("orderitem_set__product")
        .order_by("-order_date", "-id")
    )


class OrderListApiView(CustomerApiView):
    @swagger_auto_schema(tags=TAG)
    def get(self, request):
        paginator = OrderPagination()
        page = paginator.paginate_queryset(customer_orders(request.user), request)
        serializer = OrderSerializer(page, many=True, context={"request": request})
        return paginator.get_paginated_response(serializer.data)


class OrderDetailApiView(CustomerApiView):
    """One order of the customer. Other customers' orders answer 404, not 403."""

    @swagger_auto_schema(tags=TAG)
    def get(self, request, pk):
        order = customer_orders(request.user).filter(pk=pk).first()
        if order is None:
            return Response({"detail": "سفارش پیدا نشد."}, status=status.HTTP_404_NOT_FOUND)
        return Response(OrderSerializer(order, context={"request": request}).data)


class LatestOrderApiView(CustomerApiView):
    @swagger_auto_schema(tags=TAG)
    def get(self, request):
        order = customer_orders(request.user).first()
        if order is None:
            return Response({"detail": "سفارشی ثبت نشده است."}, status=status.HTTP_404_NOT_FOUND)
        return Response(OrderSerializer(order, context={"request": request}).data)
