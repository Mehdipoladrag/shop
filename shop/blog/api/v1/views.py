from django.http import HttpResponse
from django.views import View


class Test(View): 
  def get(self, request): 
    return HttpResponse('test')