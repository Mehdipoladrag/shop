from django.urls import path
from home.views import (
    HomePage, AboutPage,

)
app_name = 'home'

urlpatterns = [
    path('', HomePage.as_view(), name='home1'),
    path('about-us', AboutPage.as_view(), name='about1'),
]
