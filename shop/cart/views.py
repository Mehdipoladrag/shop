from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from cart.forms import CartAddProductForm
from .cart import Cart
from shop.models import Product
# Create your views here.


class AddCartView(View) :
    def post(self, request, product_id) : 
        cart = Cart(request) 
        product = get_object_or_404(Product, id=product_id) 
        form = CartAddProductForm(request.POST) 
        if form.is_valid() : 
            cd = form.cleaned_data
            cart.add(product=product,product_count=cd['product_count'], update_count=cd['update'])
        return redirect('cart:cart_detail')
    
class CartDeleteView(View):
    def get(self, request, product_id):
        cart = Cart(request)
        cart.remove(product_id)
        return redirect('cart:cart_detail')



class CartDetailView(View) : 
    def get(self, request) : 
        cart = Cart(request)
        if len(cart) == 0:
            return render(request, 'cart/emptycart.html')
        else : 
            for item in cart:
                item['update_product_count_form'] = CartAddProductForm(
                    initial={'product_count': item['product_count'],
                            'update': True})
            return render(request, 'cart/cart_detail.html', {'cart': cart})