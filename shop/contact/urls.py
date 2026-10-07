from django.urls import path, include

app_name = "contact"

urlpatterns = [
    path("api/v1/", include("contact.api.v1.urls")),
]
