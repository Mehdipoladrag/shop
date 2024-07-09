from django.views.generic import ListView, DetailView, View
from django.shortcuts import render, get_object_or_404
from blog.models import Category_blog, Blogs
from django.core.paginator import Paginator

# Create your views here.


# Class Base View
class BlogPageView(ListView):
    template_name = "blog/blogpage.html"
    paginate_by = 1
    model = Blogs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bloglist"] = Blogs.objects.all().order_by("create_date")
        context["categories"] = Category_blog.objects.all()
        return context


class BlogDetailView(DetailView):
    model = Blogs
    template_name = "blog/blogdetail.html"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs[self.slug_url_kwarg]
        context["blogdetail"] = Blogs.objects.get(slug=slug)
        context["categories"] = Category_blog.objects.all()
        return context


class CategoryDetailView(View):
    template_name = "blog/catdetail.html"

    def get(self, request, slug_cat):
        categor = get_object_or_404(Category_blog, slug_cat=slug_cat)
        blog_list = Blogs.objects.filter(category=categor)
        categor_list = Category_blog.objects.all()
        paginator = Paginator(blog_list, 6)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context = {
            "cat": categor,
            "blog_list": blog_list,
            "categor_list": categor_list,
            "bloglist": page_obj,
        }
        return render(request, "blog/catdetail.html", context)
