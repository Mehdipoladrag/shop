from django import forms
from contact.models import Contact
from django.forms.widgets import TextInput, EmailInput, NumberInput, Textarea



class ContactUsForm(forms.ModelForm) :
    name = forms.CharField(max_length=50, widget=TextInput(attrs={
        'placeholder': 'نام و نام خانوادگی',
        'class': 'input_second input_all',
        'label' : ' نام'
    }), label='نام و نام خانوادگی')

    email = forms.EmailField(max_length=254, widget=EmailInput(attrs={
        'placeholder': 'ایمیل',
        'class': 'input_second input_all',
    }), label='ایمیل',)

    phone = forms.IntegerField(widget=NumberInput(attrs={
        'placeholder': 'شماره تماس',
        'class': 'input_second input_all',
    }), label='شماره تماس')

    subject = forms.CharField(max_length=50, widget=TextInput(attrs={
        'placeholder': 'موضوع',
        'class': 'input_second input_all',
    }), label='موضوع')

    desc = forms.CharField(widget=Textarea(attrs={
        'placeholder': 'متن پیام',
        'class': 'input_second input_all input_textarea text-right',
        'rows': '3',
    }), label='پیام')
    
    class Meta:
        model = Contact
        fields = ('name', 'email', 'phone', 'subject','desc')
