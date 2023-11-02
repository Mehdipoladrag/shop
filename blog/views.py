from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from blog.models import Category_blog, Blogs, Visitor
from django.core.paginator import Paginator
# Create your views here.
def blog_page(request) :
    blog_list = Blogs.objects.all().order_by('create_date')
    category_blog = Category_blog.objects.all()
    paginator = Paginator(blog_list, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        'blogs' : blog_list,
        'categories': category_blog,
        'bloglist': page_obj,
    }
    return render(request, 'blog/blogpage.html', context)



def blog_detail(request, slug) : 
    blogs_details = get_object_or_404(Blogs,slug=slug)
    category_blog = Category_blog.objects.all()

    context = {
        'blogdetail' : blogs_details,
        'categories': category_blog,

    }
    return render(request,'blog/blogdetail.html', context)


def categor_detail(request, slug_cat):
    categor = get_object_or_404(Category_blog, slug_cat=slug_cat)
    blog_list = Blogs.objects.filter(category=categor)
    categor_list = Category_blog.objects.all()
    paginator = Paginator(blog_list, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        'cat': categor,
        'blog_list': blog_list,
        'categor_list': categor_list,
        'bloglist': page_obj,
    }
    return render(request, 'blog/catdetail.html', context)
