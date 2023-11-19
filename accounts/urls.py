from django.urls import path
from accounts.views import(
    signup_page, signin_page,
    user_logout, user_profile,
    user_update, change_password,
    new_address, user_message_info,
    profile2,
    ###
    ProfileUSerlistmixin, ProfileDetailmixin,
    UserListmixin,UserDetailmixin, order_list
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView
)


app_name = 'accounts'

urlpatterns = [
    path('register/', signup_page, name='signup1'),
    path('login/', signin_page, name='signin1'),
    path('logout/', user_logout, name='logout'),
    path('profile/', user_profile, name="profile1"),
    path('profile/update/', user_update, name='update1'),
    path('change-password/', change_password, name='change1'),
    path('address/', new_address, name='address1'),
    path('orders/', order_list, name='order1'),   
    path('messages/', user_message_info, name='message1'),
    path('profile2/', profile2, name='profile2'),
    
    path('api/profile-list/', ProfileUSerlistmixin.as_view()),
    path('api/profile-detail/<pk>/', ProfileDetailmixin.as_view()),
    path('api/user-list/', UserListmixin.as_view()),
    path('api/user-detail/<pk>/', UserDetailmixin.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]