from contact.forms import ContactUsForm
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib import messages


# Create your views here.
class ContactPageView(FormView):
    """
    This is a Contact View Create With FormView
    """

    template_name = "contact/contactpage.html"
    form_class = ContactUsForm
    success_url = reverse_lazy("home:home1")

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "با موفقیت ارسال شد")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "مشکلی در ارسال پیام شما به وجود آمده است")
        return super().form_invalid(form)