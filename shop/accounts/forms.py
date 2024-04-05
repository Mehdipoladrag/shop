from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm
from accounts.models import CustomUser, CustomProfileModel
from django.core.exceptions import ValidationError
from accounts.validators import UserRegisterValidators

#Signup Form
class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        max_length=25,
        validators=[UserRegisterValidators.validate_username],
        label='نام کاربری',
        widget=forms.TextInput(attrs={'placeholder': 'لطفا نام کاربری مورد نظر خود را وارد کنید', 'class': 'input_second input_all'}),
        error_messages={'required': 'لطفاً این فیلد را پر کنید'}
    )
    email = forms.EmailField(
        label='ایمیل',
        validators=[UserRegisterValidators.validate_email],
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
        #validators=[UserRegisterValidators.validate_password2],
        max_length=25,
        label='تکرار رمز عبور',
        widget=forms.PasswordInput(attrs={'placeholder': 'لطفا رمز را دوباره وارد کنید', 'class': 'input_second input_all'}),
        error_messages={'required': 'لطفاً این فیلد را پر کنید'}
    )
    class Meta :
        model = CustomUser
        fields = ('username','email', 'first_name', 'last_name', 'password1')

    
#LoginForm 
class UserLoginForm(AuthenticationForm):
    #validators=[UserLoginValidator.clean_username], 
    username = forms.CharField(max_length=25,label='نام کاربری', widget=forms.TextInput(
        attrs={'placeholder': 'لطفا نام کاربری را وارد کنید', 'class': 'input_second input_all'}))
    # validators=[UserLoginValidator.clean_password],
    password = forms.CharField(max_length=25, label='رمزعبور', widget=forms.PasswordInput(
        attrs={'placeholder': 'لطفا رمز را وارد کنید', 'class':'input_second input_all'}))
    class Meta : 
        model = CustomUser
        fields = ('username', 'password')
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            return username
        else:
            raise ValidationError('نام کاربری اشتباه است')

    def clean_password(self):
        password = self.cleaned_data.get('password')
        username = self.cleaned_data.get('username')
        if username:
            user = CustomUser.objects.filter(username=username).first()
            if user and not user.check_password(password):
                raise ValidationError('رمز عبور اشتباه است')
        return password

#Change Password Form
class UserChangePassForm(SetPasswordForm):
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = ['old_password', 'new_password1', 'new_password2']
        

# Profile Form        
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
        model = CustomProfileModel
        fields = ('national_code', 'address', 'zipcode',
                  'street', 'city', 'mobile', 'age', 'gender', 'card_number', 'iban','customer_image')


#CustomUser Form       
class CustomUserForm(forms.ModelForm) :
    username = forms.CharField(
        max_length=25,
        label='نام کاربری',
        widget=forms.TextInput(attrs={'class': 'input_second input_all'}),
        error_messages={'required': 'لطفاً این فیلد را پر کنید'}
    )
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={'class': 'input_second input_all'}),
        error_messages={'required': 'لطفاً این فیلد را پر کنید', 'invalid': 'لطفاً یک ایمیل معتبر وارد کنید'}
    )
    first_name = forms.CharField(
        max_length=25,
        label='نام',
        widget=forms.TextInput(attrs={'class': 'input_second input_all'}),
        error_messages={'required': 'لطفاً این فیلد را پر کنید'}
    )
    last_name = forms.CharField(
        max_length=25,
        label='نام خانوادگی',
        widget=forms.TextInput(attrs={'class': 'input_second input_all'}),
        error_messages={'required': 'لطفاً این فیلد را پر کنید'}
    )
    class Meta : 
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name')