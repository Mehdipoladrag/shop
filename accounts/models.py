from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import User

from django.db.models.signals import post_save
# Create your models here.
class PROFILE(models.Model):
    GENDER_CHOICES = (
        (False, 'مرد'),
        (True, 'زن'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_code = models.IntegerField(_("Code"), blank=True, null=True)
    national_code = models.CharField(_("کد ملی"), max_length=10)
    address = models.TextField(_("Address"), blank=True, null=True)
    zipcode = models.CharField(
        _("Zip Code"), max_length=20, blank=True, null=True)
    street = models.CharField(
        _("street"), max_length=20, blank=True, null=True)
    city = models.CharField(_("City"), max_length=20, blank=True, null=True)
    mobile = models.CharField(
        _("Mobile"), max_length=20, blank=True, null=True)
    age = models.PositiveIntegerField(_("Age"), blank=True, null=True)
    gender = models.BooleanField(
        _("جنسیت"), choices=GENDER_CHOICES, default=False)
    card_number = models.CharField(_("شماره کارت"), max_length=16 ,blank=True, null=True)
    iban = models.CharField(_("شماره شبا"), max_length=16 , blank=True, null=True)
    back_money = models.CharField(
        _("Back money"), max_length=50, default='شماره شبا', blank=True, null=True)
    customer_image = models.ImageField(
        _("User Image"), upload_to='images/profile/%Y/%m/%d', blank=True, null=True)
    def __str__(self):
        return self.user.username
    
def  save_profile_user(sender, **kwargs):
    if kwargs ['created']:
          profile_user=PROFILE(user=kwargs['instance'])
          profile_user.save()


post_save.connect(save_profile_user,sender=User) 