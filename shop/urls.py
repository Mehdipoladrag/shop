from django.urls import path
from shop.views import (
    shop_list, shop_detail,
    categor_list, categor_detail,
    checkout, SEARCH,
    Categorymixinlist, CategoryDetailmixin,
    Brandmixinlist, BrandDetailmixin,
    Productmixinlist, ProductDetailmixin,
    Ordermixinlist, OrderDetailmixin, 
    OrderItemmixinlist, OrderItemDetailmixin, 
    TransactionDetailmixin, Transactionmixinlist,
    Invoicemixinlist, InvoiceDetailmixin,
    offermixinlist, OfferDetailmixin,
    infoDetailmixin,infomixinlist,
    Commentxinlist, CommentDetailmixin, 
    ContactproductDetailmixin, Contactproductmixinlist
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
    path('api/product-list/', Productmixinlist.as_view()),
    path('api/product-detail/<pk>/', ProductDetailmixin.as_view()),
    path('api/order-list/', Ordermixinlist.as_view()),
    path('api/order-detail/<pk>/', OrderDetailmixin.as_view()),
    path('api/order-item-list/', OrderItemmixinlist.as_view()),
    path('api/order-item-detail/<pk>/', OrderItemDetailmixin.as_view()),
    path('api/Transaction-list/', Transactionmixinlist.as_view()),
    path('api/Transaction-detail/<pk>/', TransactionDetailmixin.as_view()),
    path('api/invoice-list/', Invoicemixinlist.as_view()),
    path('api/invoice-detail/<pk>/', InvoiceDetailmixin.as_view()),
    path('api/offer-list/', offermixinlist.as_view()),
    path('api/offer-detail/<pk>/', OfferDetailmixin.as_view()),
    path('api/info-list/', infomixinlist.as_view()),
    path('api/info-detail/<pk>/', infoDetailmixin.as_view()),
    path('api/comment-list/', Commentxinlist.as_view()),
    path('api/comment-detail/<pk>/', CommentDetailmixin.as_view()),
    path('api/contact-product-list/', Contactproductmixinlist.as_view()),
    path('api/contact-product-detail/<pk>/', ContactproductDetailmixin.as_view()),

]

