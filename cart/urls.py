from django.urls import path
from cart.views import (
    cart_detail,
    AddCartView,
    CartDeleteView,
)

app_name = 'cart'

urlpatterns = [
    path('', cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', AddCartView.as_view(), name='cart_add'),
    path('remove/<int:product_id>/', CartDeleteView.as_view(), name='cart_remove'),
]
