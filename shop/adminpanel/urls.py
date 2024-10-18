from django.urls import path, include
from .views import (
    LoginDashboard,
    CategoryDashboard,
    DashboardView,

)

app_name = "adminpanel"

urlpatterns = [
    path("login/", LoginDashboard.as_view()),
    path("dashboard/", DashboardView.as_view(), name="dashboardroat"),
    path("categories/", CategoryDashboard.as_view()),
    path("api/v2/", include("adminpanel.api.v2.urls")),
]
