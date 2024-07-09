from rest_framework import serializers
from blog.models import Blogs, Category_blog, Visitor


class BlogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blogs
        fields = "__all__"


class CategoryBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category_blog
        fields = "__all__"


class VisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitor
        fields = "__all__"
