from django.shortcuts import render, redirect
from contact.forms import ContactUsForm
from contact.models import Contact
from contact.serializers import ContactSerializer
from rest_framework import mixins, generics
from rest_framework.permissions import IsAdminUser

# Create your views here.
def contact_page(request) :
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            subject = form.cleaned_data['subject']
            desc = form.cleaned_data['desc']
            contact = Contact(name=name, email=email,phone=phone, subject=subject, desc=desc)
            contact.save() 
            return redirect('home:home1')
    else:
        form = ContactUsForm()

    return render(request, 'contact/contactpage.html',{'form': form})



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
    
