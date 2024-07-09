from django import forms
from shop.models import Contact_product


class ContactProductForm(forms.ModelForm):

    message_product = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": "متن نظر و پرسش",
                "class": "form-control",
                "rows": "4",
            }
        )
    )

    class Meta:
        model = Contact_product
        fields = ["username", "product", "message_product"]
