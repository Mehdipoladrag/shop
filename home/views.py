from django.shortcuts import render
from shop.models import Product, Brand, Category
from blog.models import Blogs 
# Create your views here.
def home_page(request) :
    productoffer = Product.objects.filter(offer__gt=0).order_by('create_date')
    productlist = Product.objects.all().exclude(pk__in=productoffer)
    categories = Category.objects.all()
    brands = Brand.objects.all()
    blog_list = Blogs.objects.all().order_by('create_date') # نمایش وبلاگ ها
    context = {
        'blogs' : blog_list,
        'brand' : brands,
        'category' : categories,
        'products': productlist,
        'productoffer': productoffer,
    }

    
    return render(request, 'home/homepage.html', context)

def about_page(request) :
    return render(request, 'home/about.html')


