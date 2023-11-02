from django.urls import path
from contact.views import (
    contact_page,
)

app_name = 'contact'

urlpatterns = [
    path('', contact_page, name='contact1'),
]
