from django.urls import path
from . import customer_views
from .views import (
    UserListApiView,
    UserProfileListApiView,
    UserUpdateApiView,
    UserCreateApiView,
    UserDeleteApiView,
    UserProfileDeleteApiView,
    UserProfileUpdateApiView,
    UserDetailApiView,
    ProfileDetailApiView,
    LoginApiView,
    UserOrderFilterApiView,
    UserIsCompleteApiView,
    UserCityFilterApiView, 
    UserMaxAgeApiView,
    UserMinAgeApiView, 
    UserNameSearchApiView,
    UserDateJoinedApiView,
)


urlpatterns = [
    # Customer area (session login, CSRF protected)
    path("customer/csrf/", customer_views.CsrfCookieApiView.as_view()),
    path("customer/register/", customer_views.RegisterApiView.as_view()),
    path("customer/login/", customer_views.LoginApiView.as_view()),
    path("customer/logout/", customer_views.LogoutApiView.as_view()),
    path("customer/profile/", customer_views.ProfileApiView.as_view()),
    path("customer/password/", customer_views.ChangePasswordApiView.as_view()),
    path("customer/address/", customer_views.AddressApiView.as_view()),
    path("customer/orders/", customer_views.OrderListApiView.as_view()),
    path("customer/orders/latest/", customer_views.LatestOrderApiView.as_view()),
    path("customer/orders/<int:pk>/", customer_views.OrderDetailApiView.as_view()),
    # List
    path("users-list/", UserListApiView.as_view()),
    path("users-profile/", UserProfileListApiView.as_view()),
    # Detail
    path("users-detail/<int:pk>/", UserDetailApiView.as_view()),
    path("users-profile-detail/<int:pk>/", ProfileDetailApiView.as_view()),
    # Update
    path("users-change-info/<int:pk>/", UserUpdateApiView.as_view()),
    path("users-change-profile/<int:pk>/", UserProfileUpdateApiView.as_view()),
    # Create
    path("users-create/", UserCreateApiView.as_view()),
    # Delete
    path("users-delete/<int:pk>/", UserDeleteApiView.as_view()),
    path("users-profile-delete/<int:pk>/", UserProfileDeleteApiView.as_view()),
    # Login
    path("login/", LoginApiView.as_view(), name="login-api"),
    # User Filters
    path("user-order/", UserOrderFilterApiView.as_view()),
    path("user-complete/", UserIsCompleteApiView.as_view()),
    path("user-city/", UserCityFilterApiView.as_view()),
    path("user-max-age/", UserMaxAgeApiView.as_view()),
    path("user-min-age/", UserMinAgeApiView.as_view()),
 
    path("users/search/username/", UserNameSearchApiView.as_view()), # Params /?name=user_name
    path("users/filter/created/", UserDateJoinedApiView.as_view()), # Params /?date=
]
