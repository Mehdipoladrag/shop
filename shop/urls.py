from django.urls import path
from shop.views import (
    shop_list, shop_detail,
    categor_list, categor_detail,
    checkout,
)
app_name = 'shop'

urlpatterns = [
    path('', shop_list, name='shoplist'),
    path('product/<slug:slug>/', shop_detail, name='detailpro'),
    path('all-categories/', categor_list, name='categorylist1'),
    path('<str:category_slug>/',categor_detail, name='categorydetail1'),
    path('payment/checkout/', checkout, name='checkout1'),
]

