from django.shortcuts import render
from shop.models import Product, Category, Brand, Comment, OrderItem, Order, Transaction, Invoice
from django.core.paginator import Paginator
from shop.forms import ContactProductForm
from django.shortcuts import render, get_object_or_404
from cart.forms import CartAddProductForm
from cart.cart import Cart
from decimal import Decimal
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from rest_framework.permissions import IsAdminUser
from rest_framework import generics,mixins
from shop.serializers import * 
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
# Create your views here.


# SHOP LISt http://127.0.0.1:8000/shop/
def shop_list(request) :
    cat = Category.objects.all()
    product_list = Product.objects.all()
    paginator = Paginator(product_list, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    brands = Brand.objects.all()
    context = {
        'product_list': product_list,
        'listpage': page_obj,
        'categori': cat,
        'brands': brands,

    }
    return render(request, 'shop/shoplist.html', context)


# PRODUCT DETAIL
def shop_detail(request, slug) :
    if request.method == 'POST':
        productform = ContactProductForm(request.POST)
        if productform.is_valid():
            productform.save()
            productform = ContactProductForm()
    else:
        productform = ContactProductForm()

    product_detail = get_object_or_404(Product,slug=slug)
    comments = Comment.objects.filter(product=product_detail)
    cart_add_product_form = CartAddProductForm()
    context = {
      
        'products': product_detail,
        'comments': comments,
        'form': productform,
        'cart_add_product_form': cart_add_product_form,
    }
    return render(request, 'shop/shopdetail.html', context)

def SEARCH(request):
    brands = Brand.objects.all()
    products2 = Product.objects.all()
    q = request.GET.get('q')
    if q:
        products = Product.objects.filter(Q(product_name__icontains=q))
        context = {
            'q': q,
            'products': products,
            'products2': products2,
            'brands' : brands,
        }
        return render(request, 'shop/search.html', context)
    return render(request, 'shop/search.html')

# http://127.0.0.1:8000/shop/all-categories/
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


def categor_detail(request, category_slug): 
    categorlist = Category.objects.exclude(category_slug=category_slug)
    categor = get_object_or_404(Category,category_slug=category_slug)

    productlist = Product.objects.filter(product_category=categor)
    paginator = Paginator(productlist, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    brands = Brand.objects.all()
    context = {
        'cat' : categor,
        'categorlist' : categorlist,
        'brand': brands,
        'listpage': page_obj,

    }
    return render(request,'shop/detailcat.html', context) 





@login_required
def checkout(request):
    cart = Cart(request)
    if not cart:
        return render(request, 'cart/emptycart.html')
    
    order = None
    if request.method == 'POST':
        order = Order.objects.create(customer=request.user)
        invoice = Invoice.objects.create(order=order, invoice_date=timezone.now())
        
        order_total_cost = Decimal('0')
        
        for item in cart:
            product = item['product']
            product_count = item['product_count']
            product_price = item['price']
            discounted_price = item['discounted_price']
            
            product_cost = Decimal(product_count) * Decimal(discounted_price)
            item['cost'] = product_cost
            order_total_cost += product_cost
            
            OrderItem.objects.create(order=order,
                                    customer=request.user,
                                    product=product,
                                    product_price=product_price,
                                    product_count=product_count,
                                    product_cost=product_cost)
        
        Transaction.objects.create(invoice=invoice,
                                   transaction_date=timezone.now(),
                                   amount=order_total_cost,
                                   status='pending')
        
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
