from django.shortcuts import render, redirect
from contact.forms import ContactUsForm
from contact.models import Contact

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


