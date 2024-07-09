from django.urls import path, include
from contact.views import (
    ContactPageView, 
)

app_name = 'contact'

urlpatterns = [
    path('', ContactPageView.as_view(), name='contact1'),
    # API 
    path('api/v1/', include('contact.api.v1.urls')),
]
