from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model 
user=get_user_model()
# Create your models here.
class PROFILE(models.Model):
    GENDER_CHOICES = (
        (False, 'مرد'),
        (True, 'زن'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='نام کاربری')
    user_code = models.IntegerField(_("کد کاربر"), blank=True, null=True)
    national_code = models.CharField(_("کد ملی"), max_length=10)
    address = models.TextField(_("آدرس"), blank=True, null=True)
    zipcode = models.CharField(
        _("کد پستی"), max_length=20, blank=True, null=True)
    street = models.CharField(
        _("خیابان"), max_length=50, blank=True, null=True)
    city = models.CharField(_("شهر"), max_length=20, blank=True, null=True)
    mobile = models.CharField(
        _("Mobile"), max_length=11, blank=True, null=True)
    age = models.PositiveIntegerField(_("سن"), blank=True, null=True)
    gender = models.BooleanField(
        _("جنسیت"), choices=GENDER_CHOICES, default=False)
    card_number = models.CharField(_("شماره کارت"), max_length=16 ,blank=True, null=True)
    iban = models.CharField(_("شماره شبا"), max_length=16 , blank=True, null=True)
    back_money = models.CharField(
        _("روش بازگشت پول"), max_length=50, default='شماره شبا', blank=True, null=True)
    customer_image = models.ImageField(
        _("عکس کاربر"), upload_to='images/profile/%Y/%m/%d', blank=True, null=True)
    def __str__(self):
        return self.user.username
    class Meta:
        verbose_name = 'پروفایل'
        verbose_name_plural  = 'پروفایل ها'
def  save_profile_user(sender, **kwargs):
    if kwargs ['created']:
          profile_user=PROFILE(user=kwargs['instance'])
          profile_user.save()


post_save.connect(save_profile_user,sender=User) 



