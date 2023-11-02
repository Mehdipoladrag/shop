from django.shortcuts import render
from shop.models import Product, Category, Brand, Comment, OrderItem, Order, Transaction, Invoice
from django.core.paginator import Paginator
from shop.forms import ContactProductForm
from django.shortcuts import render, get_object_or_404
from cart.forms import CartAddProductForm
from cart.cart import Cart
from decimal import Decimal

from django.utils import timezone
from django.contrib.auth.decorators import login_required

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
    if request.method == 'POST':
        order = Order.objects.create(customer=request.user)
        
        # ایجاد فاکتور
        invoice = Invoice.objects.create(order=order, invoice_date=timezone.now())
        
        order_total_cost = Decimal('0')  # مقدار اولیه هزینه کل سفارش
        
        for item in cart:
            product = item['product']
            product_count = item['product_count']
            product_price = item['price']
            
            product_cost = Decimal(product_count) * Decimal(product_price)
            item['cost'] = product_cost
            order_total_cost += product_cost  # افزودن هزینه هر محصول به هزینه کل سفارش
            
            OrderItem.objects.create(order=order,
                                    customer=request.user,
                                    product=product,
                                    product_price=product_price,
                                    product_count=product_count,
                                    product_cost=product_cost)
        
        # ایجاد تراکنش
        Transaction.objects.create(invoice=invoice,
                                   transaction_date=timezone.now(),
                                   amount=order_total_cost,  # استفاده از متغیر برای مقدار amount
                                   status='pending')
        
        cart.clear()
        return render(request, 'shop/final_payment.html', {'order': order})
    
    return render(request, 'shop/checkout.html', {'cart': cart})