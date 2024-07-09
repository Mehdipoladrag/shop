from contact.forms import ContactUsForm
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib import messages

# Create your views here.
class ContactPageView(FormView):
    """ 
        This is a Contact View Create With FormView 
    """
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
        
