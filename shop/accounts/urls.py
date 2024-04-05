from django.urls import path
from accounts.views import(
    SignUpView,
    LoginUserView, UserLogOutView,
    UserProfileView, ProfileUpdateView,
    UserChangePasswordView, UserAddressView, 
    user_message_info,
    # APIS
    ProfileUSerlistmixin, ProfileDetailmixin,
    UserListmixin,UserDetailmixin, 
    #
    order_list
)
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView, TokenVerifyView
# )


app_name = 'accounts'

urlpatterns = [
    
    path('register/', SignUpView.as_view(), name='signup1'),
    path('login/', LoginUserView.as_view(), name='signin1'),
    path('logout/', UserLogOutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name="profile1"),
    path('profile/update/', ProfileUpdateView.as_view(), name='update1'),
    path('change-password/', UserChangePasswordView.as_view(), name='change1'),
    path('address/', UserAddressView.as_view(), name='address1'),
    path('orders/', order_list, name='order1'),   
    path('messages/', user_message_info, name='message1'),
    path('api/v1/profile-list/', ProfileUSerlistmixin.as_view()),
    path('api/v1/profile-detail/<pk>/', ProfileDetailmixin.as_view()),
    path('api/v1/user-list/', UserListmixin.as_view()),
    path('api/v1/user-detail/<pk>/', UserDetailmixin.as_view()),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]