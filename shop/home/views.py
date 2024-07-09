from shop.models import Product, Brand, Category
from blog.models import Blogs
from django.views.generic import TemplateView, ListView

# Create your views here.

# Class Base Views


class HomePageView(ListView):
    template_name = "home/homepage.html"
    model = Product

    def get_queryset(self):
        productoffer = Product.objects.filter(offer__gt=0).order_by("create_date")
        productlist = Product.objects.all().exclude(pk__in=productoffer)
        blogs = Blogs.objects.all().order_by("create_date")
        category = Category.objects.all()
        brand = Brand.objects.all()
        return productoffer, productlist, blogs, category, brand

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        productoffer, productlist, blogs, category, brand = self.get_queryset()
        context["productoffer"] = productoffer
        context["products"] = productlist
        context["blogs"] = blogs
        context["category"] = category
        context["brand"] = brand
        return context


class AboutPageView(TemplateView):
    template_name = "home/about.html"
