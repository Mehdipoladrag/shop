from django.urls import path, include
from . import views
from contact.views import (
    ContactPageView, 
        ################
    ContactListMixin, ContactDetailMixin,
)

app_name = 'contact'

urlpatterns = [
    path('', ContactPageView.as_view(), name='contact1'),
    path('api/contact/', ContactListMixin.as_view(), name="contact_api_list"),
    path('api/contact/<pk>/', ContactDetailMixin.as_view()),
]
