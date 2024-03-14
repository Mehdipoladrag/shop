from typing import Any
from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from django.shortcuts import render, get_object_or_404
from blog.models import Category_blog, Blogs, Visitor
from django.core.paginator import Paginator
from rest_framework import generics, mixins
from blog.serializers import BlogsSerializer, CategoryBlogSerializer, VisitorSerializer
from rest_framework.permissions import IsAdminUser
# Create your views here.

# Class Base View
class BlogPage(ListView) : 
    template_name = 'blog/blogpage.html'
    paginate_by = 1
    model = Blogs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bloglist'] = Blogs.objects.all().order_by('create_date')
        context['categories'] = Category_blog.objects.all()
        return context 


class BlogDetail(DetailView) : 
    model = Blogs
    template_name = 'blog/blogdetail.html'
    slug_url_kwarg = 'slug'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs[self.slug_url_kwarg]
        context['blogdetail'] = Blogs.objects.get(slug=slug)
        context ['categories'] = Category_blog.objects.all()
        return context

# class CategoryDetail(DetailView):
#     template_name = 'blog/catdetail.html'
#     model = Category_blog
#     slug_url_kwarg = 'slug'
#     def get_context_data(self, **kwargs) :
#         context = super().get_context_data(**kwargs)
#         slug = self.kwargs[self.slug_url_kwarg]
#         categor = get_object_or_404(Category_blog, slug=slug)
#         context['cat'] = categor
#         context ['blog_list'] = Blogs.objects.filter(category=categor)
#         context ['categor_list'] = Category_blog.objects.all()
    
class CategoryDetail(View):
    template_name = 'blog/catdetail.html'
    def get(self , request, slug_cat):
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





########## API 
class BlogPermission(IsAdminUser) :
    pass
################# Blog API
class BloglistMixin(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView, BlogPermission) :
    queryset = Blogs.objects.all() 
    serializer_class = BlogsSerializer
    def get(self,request) :
        return self.list(request)
    def post(self, request) : 
        return self.create() 
    
class BlogDetailmixin(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView, BlogPermission) :
    queryset = Blogs.objects.all() 
    serializer_class = BlogsSerializer
    def get(self,request, pk) :
        return self.retrieve(request,pk) 
    def put(self, request, pk) :
        return self.update(request,pk)
    def delete(self, request,pk) :
        return self.destroy(request,pk)
######## Category Blog API
class CategoryBlogListmixin(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView, BlogPermission) : 
    queryset = Category_blog.objects.all()
    serializer_class = CategoryBlogSerializer
    def get(self,request) :
        return self.list(request)
    def post(self, request) : 
        return self.create() 

class CategoryBlogDetailmixin(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView, BlogPermission) :
    queryset = Category_blog.objects.all() 
    serializer_class = CategoryBlogSerializer
    def get(self,request, pk) :
        return self.retrieve(request,pk) 
    def put(self, request, pk) :
        return self.update(request,pk)
    def delete(self, request,pk) :
        return self.destroy(request,pk)
################## VISITOR BLOG API
class VisitorBlogListmixin(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView, BlogPermission) : 
    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer
    def get(self,request) :
        return self.list(request)
    def post(self, request) : 
        return self.create() 
    
class VisitorBlogDetailmixin(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView, BlogPermission) :
    queryset = Visitor.objects.all() 
    serializer_class = VisitorSerializer
    def get(self,request, pk) :
        return self.retrieve(request,pk) 
    def put(self, request, pk) :
        return self.update(request,pk)
    def delete(self, request,pk) :
        return self.destroy(request,pk)
    

