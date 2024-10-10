from rest_framework.generics import ListAPIView
from .serializers import CategorySerializers
from shop.models import Category
from rest_framework.permissions import IsAdminUser
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator


@method_decorator(never_cache, name="dispatch")
class CateApi(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    permission_classes = [IsAdminUser]