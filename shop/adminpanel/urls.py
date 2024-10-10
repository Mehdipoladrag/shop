from django.urls import path, include
from .views import (
    CategoryDashboard,
)

app_name = "adminpanel"

urlpatterns = [
    path("", CategoryDashboard.as_view()),
    path("api/v2/", include("adminpanel.api.v2.urls")),
]
