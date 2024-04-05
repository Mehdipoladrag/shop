from django.db import models
from django.utils.translation import gettext as _
# Create your models here.


class Contact(models.Model):
    name = models.CharField(_("نام"),max_length=50)
    email = models.EmailField(_("ایمیل"),max_length=254)
    phone = models.CharField(max_length=20, verbose_name='شماره تلفن')
    subject = models.CharField(_("موضوع"),max_length=50)
    desc = models.TextField(_("پیام"),)

    def __str__(self):
        return self.email
    class Meta:
        verbose_name = 'پیام'
        verbose_name_plural  = 'پیام ها'