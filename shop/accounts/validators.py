import unicodedata
from django.core.exceptions import ValidationError
from accounts.models import CustomUser
def is_persian(text):
  for char in text:
    if not unicodedata.category(char).startswith('Lo'):
      return False
  return True

class UserRegisterValidators:
  @staticmethod
  def validate_username(value):
    if not value:
      raise ValidationError('نام کاربری نمی‌تواند خالی باشد')
    if value[0].isdigit():
      raise ValidationError('نام کاربری نمی‌تواند با عدد شروع شود')
    if not value.startswith('@'):
      raise ValidationError('نام کاربری باید با @ شروع شود')
    if CustomUser.objects.filter(username=value).exists():
      raise ValidationError('نام کاربری تکراری است')
    return value

  def validate_email(value) : 
    if CustomUser.objects.filter(email=value) : 
      raise ValidationError('ایمیل تکراری است')
    if '@' not in value:
        raise ValidationError('لطفا ایمیل را به درستی وارد کنید')
    if value and value[0].isdigit():
      raise ValidationError('لطفا ایمیل را به درستی وارد کنید')
    return value  
  

# class UserLoginValidator:
#   def clean_username(value ,self):
#     username = self.cleaned_data.get('value')
#     if CustomUser.objects.filter(username=username).exists():
#         return username
#     else:
#         raise ValidationError('نام کاربری اشتباه است')
#   def clean_password(value ,self):
#         password = self.cleaned_data.get(value)
#         username = self.cleaned_data.get(value)
#         if username:
#             user = CustomUser.objects.filter(username=username).first()
#             if user and not user.check_password(password):
#                 raise ValidationError('رمز عبور اشتباه است')
#         return password