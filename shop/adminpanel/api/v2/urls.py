from django.urls import path 
from .views import UserCountApiView, NewOrderApiView, ProductCreateCountApiView



urlpatterns = [
    path('user-count/', UserCountApiView.as_view()),
    path('new-order/', NewOrderApiView.as_view()),
    path('product-count/', ProductCreateCountApiView.as_view()),

]
