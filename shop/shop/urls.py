from django.urls import path, include

app_name = "shop"

urlpatterns = [
    path("api/v1/", include("shop.api.v1.urls")),
]
