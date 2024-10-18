from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import CustomUser
from shop.models import Order, Product
from .serializers import (
    NewOrderSerializer,
 )

@method_decorator(never_cache, name="dispatch")
class UserCountApiView(APIView):
    def get(self, request):
        user_count = CustomUser.objects.count()  
        admin_count = CustomUser.objects.filter(is_superuser=True).count() 
        return Response({
            "counter": user_count, 
            "super_users": admin_count,
        })
    

@method_decorator(never_cache, name="dispatch")
class NewOrderApiView(ListAPIView):
    def get(self, request, *args, **kwargs):
        order_count = Order.objects.count()  
        return Response({"order_count": order_count})
    

@method_decorator(never_cache, name="dispatch")
class ProductCreateCountApiView(APIView):
    def get(self, request,*args, **kwargs):
        product_count = Product.objects.count()
        return Response({"product_count": product_count})