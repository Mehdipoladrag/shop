from django.urls import path, include
from accounts.views import(
    SignUpView,
    LoginUserView, UserLogOutView,
    UserProfileView, ProfileUpdateView,
    UserChangePasswordView, UserAddressView, 
    UserOrderView,
)



app_name = 'accounts'

urlpatterns = [
    
    path('register/', SignUpView.as_view(), name='signup1'),
    path('login/', LoginUserView.as_view(), name='signin1'),
    path('logout/', UserLogOutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name="profile1"),
    path('profile/update/', ProfileUpdateView.as_view(), name='update1'),
    path('change-password/', UserChangePasswordView.as_view(), name='change1'),
    path('address/', UserAddressView.as_view(), name='address1'),
    path('orders/', UserOrderView.as_view(), name='order1'),   
    # API 
    path('api/v1/', include('accounts.api.v1.urls')),
]