from django.urls import path
from home.views import (
    home_page, about_page,

)
from . import views
app_name = 'home'

urlpatterns = [
    path('', home_page, name='home1'),
    path('about-us', about_page, name='about1'),



]
