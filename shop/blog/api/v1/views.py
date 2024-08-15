from rest_framework import generics, mixins
from rest_framework.permissions import IsAdminUser
from blog.models import Blogs, Category_blog, Visitor
from .serializers import BlogsSerializer, CategoryBlogSerializer, VisitorSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
# Blog API
 
class BloglistMixinView(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    """
    In this class we can get the list
    of blogs and also create a new blog
    """

    queryset = Blogs.objects.all()
    serializer_class = BlogsSerializer
    permission_classes = [IsAdminUser]

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
            403: openapi.Response(description="Permission denied."),
        },
        tags=["Blog"],
    )
    @method_decorator(cache_page(60 * 30))  # Cache for 30 minutes
    # Cache With Cookies For Requested Url 
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
            403: openapi.Response(description="Permission denied."),
        },
        tags=["Blog"],
    )
    def post(self, request):
        return self.create(request)


class BlogDetailmixinView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    """
    In this class, we can read, delete, and edit the details of a blog
    """

    permission_classes = [IsAdminUser]
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
            403: openapi.Response(description="Permission denied."),
        },
        tags=["Blog"],
    )
    @method_decorator(cache_page(60 * 30))
   # Cache With Cookies For Requested Url 
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
            403: openapi.Response(description="Permission denied."),
        },
        tags=["Blog"],
    )
    def put(self, request, pk):
        return self.update(request, pk)

    @swagger_auto_schema(
        operation_summary="Delete a Blog",
        operation_description="This endpoint deletes a blog with pk.",
        responses={
            204: openapi.Response(description="Blog Successfully Deleted"),
            401: openapi.Response(
                description="Authentication credentials were not provided."
            ),
            403: openapi.Response(description="Permission denied."),
        },
        tags=["Blog"],
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

    permission_classes = [IsAdminUser]
    queryset = Category_blog.objects.all()
    serializer_class = CategoryBlogSerializer
    

    @swagger_auto_schema(
        operation_summary="List of BlogCategory",
        operation_description="Retrieve a list of all BlogCategory available",
        responses={
            200: openapi.Response(
                description="List of blogs",
                schema=CategoryBlogSerializer(many=True),
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided."
            ),
            403: openapi.Response(description="Permission denied."),
        },
        tags=["Blog Categories"],
    )
    @method_decorator(cache_page(60 * 30))
   # Cache With Cookies For Requested Url 
    def get(self, request):
        return self.list(request)

    @swagger_auto_schema(
        operation_summary="Creates a BlogCategory",
        operation_description="This Endpoint Creates a BlogCategory",
        responses={
            201: openapi.Response(
                description="BlogCategory Created",
                schema=CategoryBlogSerializer(),
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided."
            ),
            403: openapi.Response(description="Permission denied."),
        },
        tags=["Blog Categories"],
    )
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
    permission_classes = [IsAdminUser]
    queryset =  Category_blog.objects.all()
    serializer_class = CategoryBlogSerializer

    @swagger_auto_schema(
        operation_summary="Detail a BlogCategory",
        operation_description="This endpoint provides details of a BlogCategory with pk",
        responses={
            200: openapi.Response(
                description="BlogCategory information",
                schema=CategoryBlogSerializer(),
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided"
            ),
            403: openapi.Response(description="Permission denied."),
        },
        tags=["Blog Categories"],
    )
    @method_decorator(cache_page(60 * 30))
   # Cache With Cookies For Requested Url 
    def get(self, request, pk):
        return self.retrieve(request, pk)

    @swagger_auto_schema(
        operation_summary="Update a BlogCategory",
        operation_description="This endpoint updates the information of a BlogCategory with pk",
        responses={
            200: openapi.Response(
                description="BlogCategory Successfully Updated",
                schema=CategoryBlogSerializer(),
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided"
            ),
            403: openapi.Response(description="Permission denied."),
        },
        tags=["Blog Categories"],
    )
    def put(self, request, pk):
        return self.update(request, pk)

    @swagger_auto_schema(
        operation_summary="Delete a BlogCategory",
        operation_description="This endpoint deletes a BlogCategory with pk",
        responses={
            204: openapi.Response(description="BlogCategory Successfully Deleted"),
            401: openapi.Response(
                description="Authentication credentials were not provided"
            ),
            403: openapi.Response(description="Permission denied."),
        },
        tags=["Blog Categories"],
    )
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
    permission_classes = [IsAdminUser]
    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer

    @swagger_auto_schema(
        operation_summary="Visitor Count Or List",
        operation_description="This is a endpoint for Visitor List",
        responses={
            204: openapi.Response(description="Visitor List "),
            401: openapi.Response(
                description="Authentication credentials were not provided"
            ),
            403: openapi.Response(description="Permission denied."),
        },
        tags=["Visitor Blogs"],
    )
    def get(self, request):
        return self.list(request)

    @swagger_auto_schema(
        operation_summary="Create a Visitor",
        operation_description="This Endpoint Creates a Visitor",
        responses={
            201: openapi.Response(
                description="Visitor Created",
                schema=BlogsSerializer(),
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided"
            ),
            403: openapi.Response(description="Permission denied."),
        },
        tags=["Visitor Blogs"],
    )
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
    permission_classes = [IsAdminUser]
    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer

    @swagger_auto_schema(
        operation_summary="Detail a Visitor",
        operation_description="This endpoint provides details of a Visitor with pk",
        responses={
            200: openapi.Response(
                description="Visitor information",
                schema=CategoryBlogSerializer(),
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided."
            ),
            403: openapi.Response(description="Permission denied."),
        },
        tags=["Visitor Blogs"],
    )

    def get(self, request, pk):
        return self.retrieve(request, pk)

    @swagger_auto_schema(
        operation_summary="Update a Visitor",
        operation_description="This endpoint updates the information of a Visitor with pk",
        responses={
            200: openapi.Response(
                description="Visitor Successfully Updated",
                schema=CategoryBlogSerializer(),
            ),
            401: openapi.Response(
                description="Authentication credentials were not provided."
            ),
            403: openapi.Response(description="Permission denied."),
        },
        tags=["Visitor Blogs"],
    )
    def put(self, request, pk):
        return self.update(request, pk)

    @swagger_auto_schema(
        operation_summary="Delete a Visitor",
        operation_description="This endpoint deletes a Visitor with pk",
        responses={
            204: openapi.Response(description="Visitor Successfully Deleted"),
            401: openapi.Response(
                description="Authentication credentials were not provided."
            ),
            403: openapi.Response(description="Permission denied."),
        },
        tags=["Visitor Blogs"],
    )
    def delete(self, request, pk):
        return self.destroy(request, pk)
