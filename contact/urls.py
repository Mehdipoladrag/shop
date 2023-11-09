from django.urls import path, include
from . import views
from contact.views import (
    contact_page, 
        ################
    ContactListMixin, ContactDetailMixin,
)

app_name = 'contact'

urlpatterns = [
    path('', contact_page, name='contact1'),
    path('api/contact/', ContactListMixin.as_view(), name="contact_api_list"),
    path('api/contact/<pk>/', ContactDetailMixin.as_view()),
]
