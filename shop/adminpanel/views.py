from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

class CategoryDashboard(TemplateView):
    template_name = "adminpanel/category_dashboard.html"