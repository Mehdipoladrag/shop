from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from shop.models import (
    Category,
)
from .serializers import (
    CategorySerializer,
)



class CategoryGetApiView(APIView):
    """Create Api list for Category with APIVIEW"""

    permission_classes = [AllowAny]

    def get(self, request):
        query = Category.objects.all()
        serializer = CategorySerializer(query, many=True)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)


class CategoryCreateAPIView(CreateAPIView):
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
