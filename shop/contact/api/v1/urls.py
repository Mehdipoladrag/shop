from django.urls import path
from .views import (
    ContactListMixin,
    ContactDetailMixin,
)


urlpatterns = [
    path("contact-list/", ContactListMixin.as_view(), name="contact-list"),
    path("contact/<pk>/", ContactDetailMixin.as_view(), name= "contact-detail"),
]
