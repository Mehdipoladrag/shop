from django.shortcuts import render, redirect
from contact.forms import ContactUsForm
from contact.models import Contact
from contact.serializers import ContactSerializer
from rest_framework import mixins, generics
from rest_framework.permissions import IsAdminUser
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib import messages
# Create your views here.
class ContactPageView(FormView):
    template_name = 'contact/contactpage.html'
    form_class = ContactUsForm
    success_url = reverse_lazy('home:home1')
    def form_valid(self, form):
        form.save()
        success_message = 'با موفقیت ارسال شد'
        error_message = 'مشکلی در ارسال پیام شما به وجود آماده است'
        if form.errors:
            messages.error(self.request, error_message)
        else:
            messages.success(self.request, success_message)
        return super().form_valid(form)
        

#################################  API CONTACT 
class ContactPermisson(IsAdminUser) : 
    pass
class ContactListMixin(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView, ContactPermisson) : 
    queryset = Contact.objects.all().order_by('name')
    serializer_class = ContactSerializer 
    def get(self, request) : 
        return self.list(request)
    def post(self, request) : 
        return self.create(request)
    
class ContactDetailMixin(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView, ContactPermisson) : 
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    def get(self, request,pk) : 
        return self.retrieve(request,pk) 
    def put(self,request,pk) :
        return self.update(request,pk)
    def delete(self, request, pk) :
        return self.destroy(request, pk)
    
