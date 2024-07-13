from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from shop.models import (
    Category,
    Brand, 
    Product
)
from .serializers import (
    CategorySerializer,
    BrandSerializer,
    ProductSerializer, 
    ProductPostSerializer,
)


# Category
class CategoryGetApiView(APIView):
    """Create Api list for Category with APIVIEW"""

    permission_classes = [AllowAny]

    def get(self, request):
        query = Category.objects.all()
        serializer = CategorySerializer(query, many=True)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)


class CategoryCreateApiView(CreateAPIView):
    """Create Api For Category With generics.CreateAPIView For Create New Category"""

    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailApiView(RetrieveAPIView):
    """Create Category Detail Api For access pk Category"""

    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "pk"


class CategoryPutDeleteApiView(APIView):
    """Create Updata and Delete Api For Update or Delete Category"""

    permission_classes = [AllowAny]

    def put(self, request, pk):
        try:
            query = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response(
                {"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = CategorySerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        query = Category.objects.get(pk=pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Brand
class BrandGetApiView(APIView):
    """Create Api list for Brand with APIVIEW"""

    permission_classes = [AllowAny]

    def get(self, request):
        query = Brand.objects.all()
        serializer = BrandSerializer(query, many=True)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)
    

class BrandCreateApiView(CreateAPIView): 
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [AllowAny]



class BrandDetailApiView(RetrieveAPIView):
    """Create Brand Detail Api For access pk Brand"""

    permission_classes = [AllowAny]
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    lookup_field = "pk"


class BrandPutDeleteApiView(APIView):
    """Create Updata and Delete Api For Update or Delete Brand"""

    permission_classes = [AllowAny]

    def put(self, request, pk):
        try:
            query = Brand.objects.get(pk=pk)
        except Brand.DoesNotExist:
            return Response(
                {"error": "Brand not found."}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = BrandSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        query = Brand.objects.get(pk=pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Product 

class ProductGetApiView(APIView):
    """ Create Api For Product List With ApiView  """
    
    permission_classes = [AllowAny]
    def get(self, request): 
        query = Product.objects.all()
        serializer = ProductSerializer(query, many=True)
        data = serializer.data 
        return Response(data, status=status.HTTP_200_OK)
    


class ProductCreateApiView(CreateAPIView):
    """ This is a Api For Create a New Product With Api """

    queryset = Product.objects.all()
    serializer_class = ProductPostSerializer
    permission_classes = [AllowAny]