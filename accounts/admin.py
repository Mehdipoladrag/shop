from django.contrib import admin
from accounts.models import PROFILE,Message
# Register your models here.
from django.contrib.auth.admin import GroupAdmin, UserAdmin

from django.contrib.auth.models import Group, User
from django.utils.translation import gettext_lazy as _
admin.site.register(PROFILE)

class CustomGroupAdmin(GroupAdmin):
    verbose_name = _('گروه‌ها')
    verbose_name_plural = _('گروه‌ها')

# تغییر نمایشی برای مدل User
class CustomUserAdmin(UserAdmin):
    verbose_name = _('کاربران')
    verbose_name_plural = _('کاربران')

# ثبت نام مدل Group با استفاده از کلاس سفارشی شده
admin.site.unregister(Group)
admin.site.register(Group, CustomGroupAdmin)

# ثبت نام مدل User با استفاده از کلاس سفارشی شده
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.site_title = _('تشخیص هویت و مجوز دسترسی')
admin.site.site_header = _('پنل ادمین')
class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'message_date')
    list_filter = ('user',)

class MessageInline(admin.TabularInline):
    model = Message

class CustomUserAdmin(UserAdmin):
    inlines = [MessageInline]

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)