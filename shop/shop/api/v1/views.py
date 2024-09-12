from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAdminUser
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from shop.models import (
    Category,
    Brand,
    Product,
    Order,
    OrderItem,
    Invoice,
    Transaction,
)
from .serializers import (
    CategorySerializer,
    BrandSerializer,
    ProductSerializer,
    ProductPostSerializer,
    OrderSerializer,
    OrderItemSerializer,
    InvoiceSerializer,
    TransactionSerializer,
)


# Category
class CategoryGetApiView(APIView):
    """Create Api list for Category with APIVIEW"""

    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="List of Category",
        operation_description="Retrieve a list of all Category available in the system.",
        responses={
            200: openapi.Response(
                description="List of blogs",
                schema=CategorySerializer(),
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided."
            ),
            403: openapi.Response(description="Permission denied."),
        },
        tags=["Category API"],
    )
    def get(self, request):
        query = Category.objects.all()
        serializer = CategorySerializer(query, many=True)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)


class CategoryCreateApiView(CreateAPIView):
    """Create Api For Category With generics.CreateAPIView For Create New Category"""

    permission_classes = [IsAdminUser]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @swagger_auto_schema(
        operation_summary="Create a Category",
        operation_description="Create Category With Generics",
        responses={
            200: openapi.Response(
                description="Create a blog",
                schema=CategorySerializer(),
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided."
            ),
            403: openapi.Response(description="Permission denied."),
        },
        tags=["Category API"],
    )
    def post(self, request):
        return self.create(request)


class CategoryDetailApiView(RetrieveAPIView):
    """Create Category Detail Api For access pk Category"""

    permission_classes = [IsAdminUser]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "pk"

    @swagger_auto_schema(
        operation_summary="Detail a Category",
        operation_description="We can See a Detail a Category Information",
        responses={
            200: openapi.Response(
                description="Detail a blog",
                schema=CategorySerializer(),
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided."
            ),
            403: openapi.Response(description="Permission denied."),
        },
        tags=["Category API"],
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class CategoryPutDeleteApiView(APIView):
    """Create Updata and Delete Api For Update or Delete Category"""

    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Update a Category",
        operation_description="We can Update a Category Information",
        responses={
            200: openapi.Response(
                description="Update a blog",
                schema=CategorySerializer(),
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided."
            ),
            403: openapi.Response(description="Permission denied."),
        },
        tags=["Category API"],
    )
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

    @swagger_auto_schema(
        operation_summary="Delete a Category",
        operation_description="We can Delete a Category Information",
        responses={
            200: openapi.Response(
                description="Delete a blog",
                schema=CategorySerializer(),
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided."
            ),
            403: openapi.Response(description="Permission denied."),
        },
        tags=["Category API"],
    )
    def delete(self, request, pk):
        query = Category.objects.get(pk=pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Brand
class BrandGetApiView(APIView):
    """Create Api list for Brand with APIVIEW"""

    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="List of a Brand",
        operation_description="We can see a list of the Brand",
        responses={
            200: openapi.Response(
                description="Brand List",
                schema=BrandSerializer(),
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided."
            ),
            403: openapi.Response(description="Permission denied."),
        },
        tags=["Brand API"],
    )
    def get(self, request):
        query = Brand.objects.all()
        serializer = BrandSerializer(query, many=True)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)


class BrandCreateApiView(CreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Detail of a Brand",
        operation_description="We can see a Detail of the Brand",
        responses={
            200: openapi.Response(
                description="Brand List",
                schema=BrandSerializer(),
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided."
            ),
            403: openapi.Response(description="Permission denied."),
        },
        tags=["Brand API"],
    )
    def post(self, request):
        return self.create(request)


class BrandDetailApiView(RetrieveAPIView):
    """Create Brand Detail Api For access pk Brand"""

    permission_classes = [IsAdminUser]
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    lookup_field = "pk"

    @swagger_auto_schema(
        operation_summary="Detail of a Brand",
        operation_description="We can see a Detail of the Brand",
        responses={
            200: openapi.Response(
                description="Brand Detail",
                schema=BrandSerializer(),
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided."
            ),
            403: openapi.Response(description="Permission denied."),
        },
        tags=["Brand API"],
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class BrandPutDeleteApiView(APIView):
    """Create Updata and Delete Api For Update or Delete Brand"""

    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Update of a Brand",
        operation_description="We can see a Update of the Brand",
        responses={
            200: openapi.Response(
                description="Brand Update",
                schema=BrandSerializer(),
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided."
            ),
            403: openapi.Response(description="Permission denied."),
        },
        tags=["Brand API"],
    )
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

    @swagger_auto_schema(
        operation_summary="Delete of a Brand",
        operation_description="We can see a Delete of the Brand",
        responses={
            200: openapi.Response(
                description="Brand Delete",
                schema=BrandSerializer(),
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided."
            ),
            403: openapi.Response(description="Permission denied."),
        },
        tags=["Brand API"],
    )
    def delete(self, request, pk):
        query = Brand.objects.get(pk=pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Product


class ProductGetApiView(APIView):
    """Create Api For Product List With ApiView"""

    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Product List api",
        operation_description="We can see a Product list api",
        responses={
            200: openapi.Response(
                description="Product List",
                schema=ProductSerializer(),
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided."
            ),
            403: openapi.Response(description="Permission denied."),
        },
        tags=["Product API"],
    )
    def get(self, request):
        query = Product.objects.all()
        serializer = ProductSerializer(query, many=True)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)


class ProductCreateApiView(CreateAPIView):
    """This is a Api For Create a New Product With Api"""

    queryset = Product.objects.all()
    serializer_class = ProductPostSerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Product Post api",
        operation_description="We can Create a New Product api",
        responses={
            200: openapi.Response(
                description="Product Create",
                schema=ProductPostSerializer(),
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided."
            ),
            403: openapi.Response(description="Permission denied."),
        },
        tags=["Product API"],
    )
    def post(self, request):
        return self.create(request)


class ProductDetailApiView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]
    lookup_field = "pk"

    @swagger_auto_schema(
        operation_summary="Detail a Product Information api",
        operation_description="We can See a Detail product Information with this api",
        responses={
            200: openapi.Response(
                description="Product Detail",
                schema=ProductSerializer(),
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided."
            ),
            403: openapi.Response(description="Permission denied."),
        },
        tags=["Product API"],
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class ProductPutDeleteApiView(APIView):
    """Create Updata and Delete Api For Update or Delete Product"""

    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="update Product Information api",
        operation_description="We can update a product Information with this api",
        responses={
            200: openapi.Response(
                description="Product update",
                schema=ProductSerializer(),
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided."
            ),
            403: openapi.Response(description="Permission denied."),
        },
        tags=["Product API"],
    )
    def put(self, request, pk):
        try:
            query = Product.objects.get(pk=pk)
        except Brand.DoesNotExist:
            return Response(
                {"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProductSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete Product Information api",
        operation_description="We can Delete a product Information with this api",
        responses={
            200: openapi.Response(
                description="Product Delete",
                schema=ProductSerializer(),
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided."
            ),
            403: openapi.Response(description="Permission denied."),
        },
        tags=["Product API"],
    )
    def delete(self, request, pk):
        query = Product.objects.get(pk=pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Order
class OrderGetApiView(APIView):
    """Create Api For Order List With ApiView"""

    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Order Information api",
        operation_description="We can Order Information with this api",
        tags=["Order & OrderItem API"],
    )
    def get(self, request):
        query = Order.objects.all()
        serializer = OrderSerializer(query, many=True)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)


class OrderDetailApiView(RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]
    lookup_field = "pk"

    @swagger_auto_schema(
        operation_summary="Order Information Detail api",
        operation_description="We can See a Detail Order Information with this api",
        tags=["Order & OrderItem API"],
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class OrderPutDeleteApiView(APIView):
    """Create Updata and Delete Api For Update or Delete Order"""

    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Order Information Update api",
        operation_description="We can Update Order Information with this api",
        tags=["Order & OrderItem API"],
    )
    def put(self, request, pk):
        try:
            query = Order.objects.get(pk=pk)
        except Brand.DoesNotExist:
            return Response(
                {"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = OrderSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Order Information Delete api",
        operation_description="We can Delete Order Information with this api",
        tags=["Order & OrderItem API"],
    )
    def delete(self, request, pk):
        query = Order.objects.get(pk=pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# OrderItem


class OrderItemGetApiView(APIView):
    """Create Api For OrderItem List With ApiView"""

    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="OrderItem Information List api",
        operation_description="We can See a OrderItem Information list with this api",
        tags=["Order & OrderItem API"],
    )
    def get(self, request):
        query = OrderItem.objects.all()
        serializer = OrderItemSerializer(query, many=True)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)


class OrderItemDetailApiView(RetrieveAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAdminUser]
    lookup_field = "pk"

    @swagger_auto_schema(
        operation_summary="OrderItem Information Detail api",
        operation_description="We can See a OrderItem Information Detail with this api",
        tags=["Order & OrderItem API"],
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class OrderItemPutDeleteApiView(APIView):
    """Create Updata and Delete Api For Update or Delete OrderItem"""

    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="OrderItem Information Updaet api",
        operation_description="We can Update a OrderItem Information list with this api",
        tags=["Order & OrderItem API"],
    )
    def put(self, request, pk):
        try:
            query = OrderItem.objects.get(pk=pk)
        except Brand.DoesNotExist:
            return Response(
                {"error": "OrderItem not found."}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = OrderItemSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="OrderItem Information Delete api",
        operation_description="We can Delete OrderItem Information list with this api",
        tags=["Order & OrderItem API"],
    )
    def delete(self, request, pk):
        query = OrderItem.objects.get(pk=pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Invoice
class InvoiceGetApiView(APIView):
    """Create Api For Invoice List With ApiView"""

    permission_classes = [IsAdminUser]

    def get(self, request):
        query = Invoice.objects.all()
        serializer = InvoiceSerializer(query, many=True)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)


class InvoiceDetailApiView(RetrieveAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAdminUser]
    lookup_field = "pk"


class InvoicePutDeleteApiView(APIView):
    """Create Updata and Delete Api For Update or Delete Invoice"""

    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        try:
            query = Invoice.objects.get(pk=pk)
        except Brand.DoesNotExist:
            return Response(
                {"error": "Invoice not found."}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = InvoiceSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        query = Invoice.objects.get(pk=pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Transaction


class TransactionGetApiView(APIView):
    """Create Api For Transaction List With ApiView"""

    permission_classes = [IsAdminUser]

    def get(self, request):
        query = Transaction.objects.all()
        serializer = TransactionSerializer(query, many=True)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)


class TransactionDetailApiView(RetrieveAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAdminUser]
    lookup_field = "pk"


class TransactionPutDeleteApiView(APIView):
    """Create Updata and Delete Api For Update or Delete Transaction"""

    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        try:
            query = Transaction.objects.get(pk=pk)
        except Brand.DoesNotExist:
            return Response(
                {"error": "Transaction not found."}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = TransactionSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        query = Transaction.objects.get(pk=pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
