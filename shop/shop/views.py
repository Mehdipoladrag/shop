from typing import Any
from django.shortcuts import render
# Models
from shop.models import Product, Category, Brand, Comment, OrderItem, Order, Transaction, Invoice
# Serializers
from shop.serializers import * 

#
from django.views.generic import ListView, DetailView, View 
from django.core.paginator import Paginator
from shop.forms import ContactProductForm
from django.shortcuts import render, get_object_or_404
from cart.forms import CartAddProductForm
from cart.cart import Cart
from decimal import Decimal
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
# For APIS
from rest_framework.permissions import IsAdminUser
from rest_framework import generics,mixins
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
# Create your views here.


class ShopListView(ListView) : 
    template_name = 'shop/shoplist.html'
    model = Product
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_list'] = Product.objects.all()
        context['categori'] = Category.objects.all()
        context['brands'] = Brand.objects.all()
        return context


class ShopDetailView(DetailView):
    model = Product  
    template_name = 'shop/shopdetail.html'
    slug_url_kwarg = 'slug'  
    def get_context_data(self, **kwargs):
        slug = self.kwargs.get(self.pk_url_kwarg)
        context = super().get_context_data(**kwargs)
        product_detail = self.object  
        context['products'] = product_detail
        context['cart_add_product_form'] = CartAddProductForm()
        #context['comments'] = Comment.objects.filter(product=product_detail)
        return context


class SearchView(View) : 
    def get(self, request) : 
        brands = Brand.objects.all()
        products2 = Product.objects.all()
        q = request.GET.get('q') 
        if q : 
            products = Product.objects.filter(Q(product_name__icontains=q))
            context = {
            'q': q,
            'products': products,
            'products2': products2,
            'brands' : brands,
        }
            return render(request, 'shop/search.html', context)
        return render(request, 'shop/search.html')

def categor_list(request):
    product_list = Product.objects.filter(offer__gt=0).order_by('create_date')
    product_second_list = Product.objects.filter(product_rate__gt=0).exclude(pk__in=product_list)
    categor = Category.objects.all()
    brands = Brand.objects.all()
    context = {
        'cat' : categor,
        'brand' : brands,
        'products': product_list,
        'product2': product_second_list,
    }
    return render(request, 'shop/categoryproductlist.html', context)


class CategoryListView(ListView):
    model = Product
    template_name = 'shop/categoryproductlist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(offer__gt=0).order_by('create_date')
        product_list_ids = list(context['products'].values_list('pk', flat=True))
        context['product2'] = Product.objects.filter(product_rate__gt=0).exclude(pk__in=product_list_ids)
        context['cat'] = Category.objects.all()
        context['brand'] = Brand.objects.all()
        return context
class CategoryDetailView(DetailView):
    model = Category
    template_name = 'shop/detailcat.html'
    context_object_name = 'cat'
    slug_url_kwarg = 'category_slug' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        context['categorlist'] = Category.objects.exclude(pk=category.pk)
        productlist = Product.objects.filter(product_category=category)
        paginator = Paginator(productlist, 9)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['brand'] = Brand.objects.all()
        context['listpage'] = page_obj
        return context

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        slug = self.kwargs.get(self.slug_url_kwarg)
        if slug is not None:
            queryset = queryset.filter(category_slug=slug)
        obj = get_object_or_404(queryset)
        return obj
    
class CheckOutView(LoginRequiredMixin,View) : 
    def get(self, request):
        cart = Cart(request) 
        if not cart: 
            return render(request, 'cart/emptycart.html')
        return render(request, 'shop/checkout.html', {'cart': cart})
    def post(self, request):
        cart = Cart(request) 
        order = None
        order_total_cost = Decimal('0')
        order_items = []       
        print("Total Cost:", order_total_cost)
        if request.method == 'POST':
            order = Order.objects.create(customer=request.user)
            invoice = Invoice.objects.create(order=order, invoice_date=timezone.now())
            for item in cart:
                product = item['product']
                product_count = item['product_count']
                product_price = item['price']
                discounted_price = item['discounted_price']
                
                product_cost = Decimal(product_count) * Decimal(discounted_price)
                item['cost'] = product_cost
                order_total_cost += product_cost
                
                order_items.append(OrderItem(order=order,
                                            customer=request.user,
                                            product=product,
                                            product_price=product_price,
                                            product_count=product_count,
                                            product_cost=product_cost))
            
            Transaction.objects.create(invoice=invoice,
                                    transaction_date=timezone.now(),
                                    amount=order_total_cost,
                                    status='pending')
            
            OrderItem.objects.bulk_create(order_items)  # ایجاد همه آیتم‌های سفارش در یک بار
            
            cart.clear()
            return render(request, 'shop/final_payment.html', {'order': order, 'total_cost': order_total_cost})
        
        return render(request, 'shop/checkout.html', {'cart': cart})

@login_required
def checkout(request):
    cart = Cart(request)
    if not cart:
        return render(request, 'cart/emptycart.html')
    
    order = None
    order_total_cost = Decimal('0')
    order_items = []  # لیستی برای ذخیره آیتم‌های سفارش
    
    if request.method == 'POST':
        order = Order.objects.create(customer=request.user)
        invoice = Invoice.objects.create(order=order, invoice_date=timezone.now())
        
        for item in cart:
            product = item['product']
            product_count = item['product_count']
            product_price = item['price']
            discounted_price = item['discounted_price']
            
            product_cost = Decimal(product_count) * Decimal(discounted_price)
            item['cost'] = product_cost
            order_total_cost += product_cost
            
            order_items.append(OrderItem(order=order,
                                         customer=request.user,
                                         product=product,
                                         product_price=product_price,
                                         product_count=product_count,
                                         product_cost=product_cost))
        
        Transaction.objects.create(invoice=invoice,
                                   transaction_date=timezone.now(),
                                   amount=order_total_cost,
                                   status='pending')
        
        OrderItem.objects.bulk_create(order_items)  # ایجاد همه آیتم‌های سفارش در یک بار
        
        cart.clear()
        return render(request, 'shop/final_payment.html', {'order': order, 'total_cost': order_total_cost})
    
    return render(request, 'shop/checkout.html', {'cart': cart})


########## API 
class ShopPermission(IsAdminUser) :
    pass 
### Category API 
class Categorymixinlist(mixins.ListModelMixin,mixins.CreateModelMixin, generics.GenericAPIView,ShopPermission) :
    queryset = Category.objects.all()
    serializer_class = CategorySerializer 
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filterset_fields = ['category_name']
    search_fields = ['category_name']
    ordering_fields = ['category_name']
    ordering_fields = '__all__'
    def get(self,request) :
        return self.list(request)
    def post(self, request) :
        return self.create(request) 
    
class CategoryDetailmixin(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,mixins.DestroyModelMixin, generics.GenericAPIView,ShopPermission) :
    queryset = Category.objects.all()
    serializer_class = CategorySerializer 
    def get(self, request, pk) :
        return self.retrieve(request,pk)
    def put(self, request, pk) :
        return self.update(request,pk)
    def delete(self,request,pk) :
        return self.destroy(request, pk)
## Brand API 
class Brandmixinlist(mixins.ListModelMixin,mixins.CreateModelMixin, generics.GenericAPIView,ShopPermission) :
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer 
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filterset_fields = ['brand_name']
    search_fields = ['brand_name',]
    ordering_fields = ['brand_name']
    ordering_fields = '__all__'
    def get(self,request) :
        return self.list(request)
    def post(self, request) :
        return self.create(request) 
    
class BrandDetailmixin(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,mixins.DestroyModelMixin, generics.GenericAPIView,ShopPermission) :
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer 
    def get(self, request, pk) :
        return self.retrieve(request,pk)
    def put(self, request, pk) :
        return self.update(request,pk)
    def delete(self,request,pk) :
        return self.destroy(request, pk)
### Product    
class Productmixinlist(mixins.ListModelMixin,mixins.CreateModelMixin, generics.GenericAPIView,) :
    queryset = Product.objects.all().order_by('-create_date')
    serializer_class = ProductSerializer 
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filterset_fields = ['product_name']
    search_fields = ['product_name',]
    ordering_fields = ['create_date']
    ordering_fields = '__all__'
    def get(self,request) :
        return self.list(request)
    def post(self, request) :
        return self.create(request) 
    
class ProductDetailmixin(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,mixins.DestroyModelMixin, generics.GenericAPIView,ShopPermission) :
    queryset = Product.objects.all()
    serializer_class = ProductSerializer 
    def get(self, request, pk) :
        return self.retrieve(request,pk)
    def put(self, request, pk) :
        return self.update(request,pk)
    def delete(self,request,pk) :
        return self.destroy(request, pk)
# ORder API
class Ordermixinlist(mixins.ListModelMixin,mixins.CreateModelMixin, generics.GenericAPIView,ShopPermission) :
    queryset = Order.objects.all()
    serializer_class = OrderSerializer 
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filterset_fields = ['customer']
    search_fields = ['customer',]
    ordering_fields = ['order_date']
    ordering_fields = '__all__'
    def get(self,request) :
        return self.list(request)
    def post(self, request) :
        return self.create(request) 
    
class OrderDetailmixin(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,mixins.DestroyModelMixin, generics.GenericAPIView,ShopPermission) :
    queryset = Order.objects.all()
    serializer_class = OrderSerializer 
    def get(self, request, pk) :
        return self.retrieve(request,pk)
    def put(self, request, pk) :
        return self.update(request,pk)
    def delete(self,request,pk) :
        return self.destroy(request, pk)
# ORDER ITEM API
class OrderItemmixinlist(mixins.ListModelMixin,mixins.CreateModelMixin, generics.GenericAPIView,ShopPermission) :
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer 
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filterset_fields = ['order']
    search_fields = ['customer',]
    ordering_fields = ['product']
    ordering_fields = '__all__'
    def get(self,request) :
        return self.list(request)
    def post(self, request) :
        return self.create(request) 
    
class OrderItemDetailmixin(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,mixins.DestroyModelMixin, generics.GenericAPIView,ShopPermission) :
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer 
    def get(self, request, pk) :
        return self.retrieve(request,pk)
    def put(self, request, pk) :
        return self.update(request,pk)
    def delete(self,request,pk) :
        return self.destroy(request, pk)
# Transaction api 
class Transactionmixinlist(mixins.ListModelMixin,mixins.CreateModelMixin, generics.GenericAPIView,ShopPermission) :
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer 
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filterset_fields = ['status',]
    search_fields = ['status',]
    ordering_fields = ['status']
    ordering_fields = '__all__'
    def get(self,request) :
        return self.list(request)
    def post(self, request) :
        return self.create(request) 
    
class TransactionDetailmixin(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,mixins.DestroyModelMixin, generics.GenericAPIView,ShopPermission) :
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer 
    def get(self, request, pk) :
        return self.retrieve(request,pk)
    def put(self, request, pk) :
        return self.update(request,pk)
    def delete(self,request,pk) :
        return self.destroy(request, pk)
## INVOICE API 
class Invoicemixinlist(mixins.ListModelMixin,mixins.CreateModelMixin, generics.GenericAPIView,ShopPermission) :
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer 
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filterset_fields = ['order',]
    search_fields = ['status',]
    ordering_fields = ['invoice_date']
    ordering_fields = '__all__'
    def get(self,request) :
        return self.list(request)
    def post(self, request) :
        return self.create(request) 
    
class InvoiceDetailmixin(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,mixins.DestroyModelMixin, generics.GenericAPIView,ShopPermission) :
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer 
    def get(self, request, pk) :
        return self.retrieve(request,pk)
    def put(self, request, pk) :
        return self.update(request,pk)
    def delete(self,request,pk) :
        return self.destroy(request, pk)
     
#API OFFER < INFO < COMMENT < CONTACT_PRODUCT

class offermixinlist(mixins.ListModelMixin,mixins.CreateModelMixin, generics.GenericAPIView,ShopPermission) :
    queryset = Offers.objects.all()
    serializer_class = OffersSerializer
    def get(self,request) :
        return self.list(request)
    def post(self, request) :
        return self.create(request) 
    
class OfferDetailmixin(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,mixins.DestroyModelMixin, generics.GenericAPIView,ShopPermission) :
    queryset = Offers.objects.all()
    serializer_class = OffersSerializer
    def get(self, request, pk) :
        return self.retrieve(request,pk)
    def put(self, request, pk) :
        return self.update(request,pk)
    def delete(self,request,pk) :
        return self.destroy(request, pk)
#API info 
class infomixinlist(mixins.ListModelMixin,mixins.CreateModelMixin, generics.GenericAPIView,ShopPermission) :
    queryset = Info.objects.all()
    serializer_class = InfoSerializer
    def get(self,request) :
        return self.list(request)
    def post(self, request) :
        return self.create(request) 
    
class infoDetailmixin(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,mixins.DestroyModelMixin, generics.GenericAPIView,ShopPermission) :
    queryset = Info.objects.all()
    serializer_class = InfoSerializer
    def get(self, request, pk) :
        return self.retrieve(request,pk)
    def put(self, request, pk) :
        return self.update(request,pk)
    def delete(self,request,pk) :
        return self.destroy(request, pk)
#API Comment 
class Commentxinlist(mixins.ListModelMixin,mixins.CreateModelMixin, generics.GenericAPIView,ShopPermission) :
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    def get(self,request) :
        return self.list(request)
    def post(self, request) :
        return self.create(request) 
    
class CommentDetailmixin(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,mixins.DestroyModelMixin, generics.GenericAPIView,ShopPermission) :
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    def get(self, request, pk) :
        return self.retrieve(request,pk)
    def put(self, request, pk) :
        return self.update(request,pk)
    def delete(self,request,pk) :
        return self.destroy(request, pk)
# Contact_product 
class Contactproductmixinlist(mixins.ListModelMixin,mixins.CreateModelMixin, generics.GenericAPIView,ShopPermission) :
    queryset = Contact_product.objects.all()
    serializer_class = ContactProductSerializer
    def get(self,request) :
        return self.list(request)
    def post(self, request) :
        return self.create(request) 
    
class ContactproductDetailmixin(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,mixins.DestroyModelMixin, generics.GenericAPIView,ShopPermission) :
    queryset = Contact_product.objects.all()
    serializer_class = ContactProductSerializer
    def get(self, request, pk) :
        return self.retrieve(request,pk)
    def put(self, request, pk) :
        return self.update(request,pk)
    def delete(self,request,pk) :
        return self.destroy(request, pk)
