from django.urls import path
from home.views import (
    Homepage, AboutPage,

)
app_name = 'home'

urlpatterns = [
    path('', Homepage.as_view(), name='home1'),
    path('about-us', AboutPage.as_view(), name='about1'),
]
