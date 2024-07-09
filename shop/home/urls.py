from django.urls import path
from home.views import (
    HomePageView,
    AboutPageView,
)

app_name = "home"

urlpatterns = [
    path("", HomePageView.as_view(), name="home1"),
    path("about-us", AboutPageView.as_view(), name="about1"),
]
