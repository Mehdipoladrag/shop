from rest_framework import generics, mixins
from rest_framework.permissions import AllowAny
from blog.models import Blogs, Category_blog, Visitor
from .serializers import BlogsSerializer, CategoryBlogSerializer, VisitorSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# Blog API


class BloglistMixinView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    """
    In this class we can get the list
    of blogs and also create a new blog
    """

    queryset = Blogs.objects.all()
    serializer_class = BlogsSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="List of blogs",
        operation_description="Retrieve a list of all blogs available in the system.",
        responses={
            200: openapi.Response(
                description="List of blogs",
                schema=BlogsSerializer(many=True),
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided."
            ),
            403: openapi.Response(
                description="Permission denied."
            ),
        },
    )
    def get(self, request):
        return self.list(request)

    @swagger_auto_schema(
        operation_summary="Creates a blog",
        operation_description="This Endpoint Creates a blog",
        responses={
            201: openapi.Response(
                description="Blog Created",
                schema=BlogsSerializer(),
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided."
            ),
            403: openapi.Response(
                description="Permission denied."
            ),
        }
    )
    def post(self, request):
        return self.create(request)

class BlogDetailmixinView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    """
    In this class, we can read, delete, and edit the details of a blog
    """
    permission_classes =[AllowAny]
    queryset = Blogs.objects.all()
    serializer_class = BlogsSerializer

    @swagger_auto_schema(
        operation_summary="Detail a Blog",
        operation_description="This endpoint provides details of a blog with pk.",
        responses={
            200: openapi.Response(
                description="Blog information",
                schema=BlogsSerializer(),
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided."
            ),
            403: openapi.Response(
                description="Permission denied."
            ),
        }
    )
    def get(self, request, pk):
        return self.retrieve(request, pk)

    @swagger_auto_schema(
        operation_summary="Update a Blog",
        operation_description="This endpoint updates the information of a blog with pk.",
        responses={
            200: openapi.Response(
                description="Blog Successfully Updated",
                schema=BlogsSerializer(),
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided."
            ),
            403: openapi.Response(
                description="Permission denied."
            ),
        }
    )
    def put(self, request, pk):
        return self.update(request, pk)

    @swagger_auto_schema(
        operation_summary="Delete a Blog",
        operation_description="This endpoint deletes a blog with pk.",
        responses={
            204: openapi.Response(
                description="Blog Successfully Deleted"
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided."
            ),
            403: openapi.Response(
                description="Permission denied."
            ),
        }
    )
    def delete(self, request, pk):
        return self.destroy(request, pk)


# Category Blog API


class CategoryBlogListmixinView(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    """
    In this class we can get the list
    of Categories and also create a new blog
    """

    queryset = Category_blog.objects.all()
    serializer_class = CategoryBlogSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create()


class CategoryBlogDetailmixinView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    """
    In this class, we can read and
    delete and edit the details of a Categories
    """

    queryset = Category_blog.objects.all()
    serializer_class = CategoryBlogSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk)

    def put(self, request, pk):
        return self.update(request, pk)

    def delete(self, request, pk):
        return self.destroy(request, pk)


# VISITOR BLOG API


class VisitorBlogListmixinView(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    """
    In this class we can get the list
    of Visitor and also create a new blog
    """

    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create()


class VisitorBlogDetailmixinView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    """
    In this class, we can read and
    delete and edit the details of a Visitor
    """

    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk)

    def put(self, request, pk):
        return self.update(request, pk)

    def delete(self, request, pk):
        return self.destroy(request, pk)
