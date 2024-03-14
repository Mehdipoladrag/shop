from typing import Any
from django.shortcuts import render
from shop.models import Product, Brand, Category
from blog.models import Blogs 
from django.views.generic import TemplateView, ListView
# Create your views here.

# Class Base Views

class Homepage(ListView):
    template_name = 'home/homepage.html'
    model = Product
    def get_queryset(self):
        productoffer = Product.objects.filter(offer__gt=0).order_by('create_date')
        productlist = Product.objects.all().exclude(pk__in=productoffer)
        return productlist
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        productoffer = Product.objects.filter(offer__gt=0).order_by('create_date')
        productlist = self.get_queryset()  
        context['products'] = productlist 
        context['productoffer'] = productoffer
        context['category'] = Category.objects.all()
        context['brand'] = Brand.objects.all()
        context['blogs'] = Blogs.objects.all().order_by('create_date')
        return context



class AboutPage(TemplateView) :
    template_name = 'home/about.html'


