from django.urls import path
from shop.views import (
    shop_list, shop_detail,
    categor_list, categor_detail,
    checkout, SEARCH,
    #####
    Categorymixinlist, CategoryDetailmixin,
    ##
    Brandmixinlist, BrandDetailmixin,
)
app_name = 'shop'

urlpatterns = [
    path('', shop_list, name='shoplist'),
    path('search/', SEARCH, name='search1'),
    path('product/<slug:slug>/', shop_detail, name='detailpro'),
    path('all-categories/', categor_list, name='categorylist1'),
    path('<str:category_slug>/',categor_detail, name='categorydetail1'),
    path('payment/checkout/', checkout, name='checkout1'),
    path('api/category-list/', Categorymixinlist.as_view()),
    path('api/category-detail/<pk>/', CategoryDetailmixin.as_view()),
    path('api/brand-list/', Brandmixinlist.as_view()),
    path('api/brand-detail/<pk>/', BrandDetailmixin.as_view()),






]

