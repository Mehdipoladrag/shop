from django.urls import path, include

app_name = "adminpanel"

urlpatterns = [
    path("api/v2/", include("adminpanel.api.v2.urls")),
]
