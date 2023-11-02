from django.urls import path
from accounts.views import(
    signup_page, signin_page,
    user_logout, user_profile,
    user_update, change_password,
    new_address,
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








]
