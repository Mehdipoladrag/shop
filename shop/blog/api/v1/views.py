from rest_framework import generics, mixins
from .serializers import BlogsSerializer, CategoryBlogSerializer, VisitorSerializer
from rest_framework.permissions import AllowAny
from blog.models import * 

# API 



# Blog API
class BloglistMixin(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView) :
  queryset = Blogs.objects.all() 
  serializer_class = BlogsSerializer
  permission_classes = [AllowAny]
  def get(self,request) :
    return self.list(request)
  def post(self, request) : 
    return self.create() 
  
class BlogDetailmixin(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView) :
    queryset = Blogs.objects.all() 
    serializer_class = BlogsSerializer
    def get(self,request, pk) :
        return self.retrieve(request,pk) 
    def put(self, request, pk) :
        return self.update(request,pk)
    def delete(self, request,pk) :
        return self.destroy(request,pk)
    
