from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
# Create your views here.

@method_decorator(never_cache, name="dispatch")
class CategoryDashboard(TemplateView):
    template_name = "adminpanel/category_dashboard.html"

@method_decorator(never_cache, name="dispatch")
class LoginDashboard(TemplateView):
    template_name = "adminpanel/login.html"
    
@method_decorator(never_cache, name='dispatch')
class DashboardView(TemplateView): 
    template_name = "adminpanel/index.html"
    