from django import forms
import unicodedata


def is_persian(text):
    for char in text:
        if not unicodedata.category(char).startswith("Lo"):
            return False
    return True


class ContactValidators:
    def validate_email(value):
        if "@" not in value:
            raise forms.ValidationError("لطفا ایمیل را به درستی وارد کنید")
        if value and value[0].isdigit():
            raise forms.ValidationError("لطفا ایمیل را به درستی وارد کنید")
        return value

    def validate_phone(value):
        if not str(value).isdigit():
            raise forms.ValidationError("لطفاً تلفن همراه خود را به درستی وارد کنید")
        if len(str(value)) != 10:
            raise forms.ValidationError("لطفاً تلفن همراه خود را به درستی وارد کنید")
        return value
