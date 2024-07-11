from rest_framework import generics, mixins
from rest_framework.permissions import AllowAny
from blog.models import Blogs, Category_blog, Visitor
from .serializers import BlogsSerializer, CategoryBlogSerializer, VisitorSerializer

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
    permission_classes = [AllowAny]

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create()


class BlogDetailmixinView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    """
    In this class, we can read and
    delete and edit the details of a blog
    """

    queryset = Blogs.objects.all()
    serializer_class = BlogsSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk)

    def put(self, request, pk):
        return self.update(request, pk)

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
