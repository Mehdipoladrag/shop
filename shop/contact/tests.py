from django.test import TestCase, SimpleTestCase
from contact.models import Contact
from django.urls import reverse, resolve
from .views import ContactPageView
from .forms import ContactUsForm
from django.contrib.messages import get_messages
# Create your tests here.

class ContactModelTest(TestCase):
    def test_create_message(self):
        # Create a new Contact object
        self.contact = Contact.objects.create(
            name="mehdi",
            email="mehdiPoladrag@gmail.com",
            phone="09351234321",
            subject="Test Subject",
            desc="Test Description"
        )
        
        retrieved_contact = Contact.objects.get(id=self.contact.id)

        self.assertEqual(retrieved_contact.name, "mehdi")
        self.assertEqual(retrieved_contact.email, "mehdiPoladrag@gmail.com")
        self.assertEqual(retrieved_contact.phone, "09351234321")
        self.assertEqual(retrieved_contact.subject, "Test Subject")
        self.assertEqual(retrieved_contact.desc, "Test Description")

        self.assertEqual(Contact.objects.count(), 1)


class UrlTest(SimpleTestCase):
    """
        SimpleTestCase It is given for tests without a database
    """
    def test_contact_url_reslove(self):
        url = reverse("contact:contact1")
        self.assertEqual(
            resolve(url).func.view_class, ContactPageView
        )


class FormTest(TestCase):
    """
        We Need To Use a Persian Subject and Message 
        Because We Validate Form with a 
        Persian Words In Forms.
    """
    def test_form_with_valid_data(self):
        form = ContactUsForm(data={
            "name": "Admin Mehdi",
            "email": "mehdi@gmail.com",
            "phone": "09354323212",
            "subject": "موضوع تست",
            "desc": "پیام تست"
        })
        self.assertTrue(form.is_valid())

    def test_from_with_no_data(self): 
        form =ContactUsForm(data={})
        self.assertFalse(form.is_valid())
     
    def test_form_with_invalid_data(self): 
        form = ContactUsForm(data={
            "name": "Admin Mehdi",
            "email": "mehdigmail.com",
            "phone": "09354323212",
            "subject": "موضوع تست",
            "desc": "پیام تست"
        })
        email_errors = form.errors.get('email', [])
        self.assertIn('Enter a valid email address.', email_errors)
        self.assertIn('لطفا ایمیل را به درستی وارد کنید', email_errors)
        


class ContactViewTest(TestCase): 
    def test_contact_get_view(self):     
        response = self.client.get(reverse('contact:contact1'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact/contactpage.html')

        self.assertIn('form', response.context)
 
        self.assertIsInstance(response.context['form'], ContactUsForm)

    def test_contact_post_data_view(self): 
        response = self.client.post(reverse('contact:contact1'), {
            'name': 'mehdi',
            'email': 'mehdi@gmail.com',
            'phone': '09354323212',
            'subject': 'TestSubject',
            'desc': 'TestDesc'
        })
        self.assertEqual(response.status_code, 302)
        messages_list = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(str(messages_list[0]), 'با موفقیت ارسال شد')
        self.assertRedirects(response, reverse('home:home1'))


    def test_contact_view_with_invalid_data(self):
        response = self.client.post(reverse('contact:contact1'), {
            'name': 'Admin Mehdi',
            'email': 'mehdigmail.com', 
            'phone': '09354323212',
            'subject': 'موضوع تست',
            'desc': 'پیام تست',
        })

        self.assertEqual(response.status_code, 200)

        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertIn('مشکلی در ارسال پیام شما به وجود آمده است', str(messages_list[0].message))