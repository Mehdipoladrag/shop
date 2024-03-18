from django import forms
from django.contrib.auth.models import User
#from accounts.models import PROFILE
class UserRegisterForm(forms.Form):
    user_name = forms.CharField(
        max_length=25,
        label='نام کاربری',
        widget=forms.TextInput(attrs={'placeholder': 'لطفا نام کاربری را وارد کنید', 'class': 'input_second input_all'}),
        error_messages={'required': 'لطفاً این فیلد را پر کنید'}
    )
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={'placeholder': 'لطفا ایمیل خود را وارد کنید', 'class': 'input_second input_all'}),
        error_messages={'required': 'لطفاً این فیلد را پر کنید', 'invalid': 'لطفاً یک ایمیل معتبر وارد کنید'}
    )
    first_name = forms.CharField(
        max_length=25,
        label='نام',
        widget=forms.TextInput(attrs={'placeholder': 'لطفا نام را وارد کنید', 'class': 'input_second input_all'}),
        error_messages={'required': 'لطفاً این فیلد را پر کنید'}
    )
    last_name = forms.CharField(
        max_length=25,
        label='نام خانوادگی',
        widget=forms.TextInput(attrs={'placeholder': 'لطفا نام خانوادگی را وارد کنید', 'class': 'input_second input_all'}),
        error_messages={'required': 'لطفاً این فیلد را پر کنید'}
    )
    password1 = forms.CharField(
        max_length=25,
        label='رمزعبور',
        widget=forms.PasswordInput(attrs={'placeholder': 'لطفا رمز عبور را وارد کنید', 'class': 'input_second input_all'}),
        error_messages={'required': 'لطفاً این فیلد را پر کنید'}
    )
    password2 = forms.CharField(
        max_length=25,
        label='تکرار رمز عبور',
        widget=forms.PasswordInput(attrs={'placeholder': 'لطفا رمز را دوباره وارد کنید', 'class': 'input_second input_all'}),
        error_messages={'required': 'لطفاً این فیلد را پر کنید'}
    )


    def clean_user_name(self):
        user = self.cleaned_data['user_name']
        if User.objects.filter(username=user).exists():
            raise forms.ValidationError(' نام کاربری تکراری است ')
        elif not user.isascii():
            raise forms.ValidationError('نام کاربری باید به زبان انگلیسی باشد')
        return user


    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('ایمیل تکراری است')
        return email

    def clean_password2(self):
        pass1 = self.cleaned_data['password1']
        pass2 = self.cleaned_data['password2']
        if pass1 != pass2:
            raise forms.ValidationError('رمز با تکرار آن برابر نیست')
        elif len(pass2) < 8:
            raise forms.ValidationError(
                ' رمز عبور شما باید بیشتر از 8 حرف باشد ')
        elif not any(x.isupper() for x in pass2):
            raise forms.ValidationError(
                ' رمز عبور شما باید شامل یک حرف بزرگ داشته باشد ')
        return pass2


class UserLoginForm(forms.Form):
    user_name = forms.CharField(max_length=25, label='نام کاربری', widget=forms.TextInput(
        attrs={'placeholder': 'لطفا نام کاربری را وارد کنید', 'class': 'input_second input_all'}))
    password1 = forms.CharField(max_length=25, label='رمزعبور', widget=forms.PasswordInput(
        attrs={'placeholder': 'لطفا رمز را وارد کنید', 'class':'input_second input_all'}))

    def clean_user_name(self):
        user_name = self.cleaned_data['user_name']
        if User.objects.filter(username=user_name).exists():
            return user_name
        else:
            raise forms.ValidationError('نام کاربری اشتباه است')

    def clean_password(self):
        password = self.cleaned_data['password1']
        user_name = self.cleaned_data.get('user_name')
        if user_name:
            user = User.objects.filter(username=user_name).first()
            if user and not user.check_password(password):
                raise forms.ValidationError('رمز عبور اشتباه است')
        return password


class UserUpdateForm(forms.ModelForm):

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input_second input_all'}), label='نام', required=True,
        error_messages={'required': 'لطفاً نام خود را وارد کنید.'})
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input_second input_all'}), label='نام خانوادگی', required=True,
        error_messages={'required': 'لطفاً نام خانوادگی خود را وارد کنید.'})
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'input_second input_all'}), label='ایمیل', required=True,
        error_messages={'required': 'لطفاً ایمیل خود را وارد کنید.'})

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')


class ProfileUpdateForm(forms.ModelForm):
    GENDER_CHOICES = (
        (False, 'مرد'),
        (True, 'زن'),
    )
    national_code = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input_second input_all'}), label='کد ملی', required=True,
        error_messages={'required': 'لطفاً کد ملی خود را وارد کنید.'})
    address = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input_second input_all'}), label='آدرس', required=True,
        error_messages={'required': 'لطفاً آدرس خود را وارد کنید.'})
    zipcode = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input_second input_all'}), label='کد پستی', required=True,
        error_messages={'required': 'لطفاً کد پستی خود را وارد کنید.'})
    street = forms.CharField(widget=forms.TextInput(attrs={'class': 'input_second input_all'}), label='خیابان',)
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'input_second input_all'}), label='شهر',)
    mobile = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'input_second input_all'}), label='شماره همراه',)
    age = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'input_second input_all'}), label='سن',)
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES, widget=forms.Select(attrs={'class': 'input_second input_all'}), label='جنسیت',)
    card_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input_second input_all'}), label='شماره کارت',)
    iban = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'input_second input_all'}), label='شماره شبا',)
    customer_image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'input_second input_all'}), label='تصویر مشتری')
    class Meta:
        #model = PROFILE
        fields = ('national_code', 'address', 'zipcode',
                  'street', 'city', 'mobile', 'age', 'gender', 'card_number', 'iban','customer_image')
