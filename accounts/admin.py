from django.contrib import admin
from accounts.models import CustomUser, CustomProfileModel
from django.utils.translation import gettext_lazy as _
from accounts.resources import UserResource, ProfileResource
from import_export.admin import ImportExportModelAdmin

#

class CustomUserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('uuid', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    list_display_links = ('username', 'email',)
    resource_class = UserResource
    search_fields = ['first_name', 'last_name', 'username']
    list_filter = ('is_staff','date_joined',)
    list_per_page = 10
    readonly_fields = ('uuid','username', 'first_name', 'last_name','is_staff','password','date_joined','last_login',)
    # FieldSets 
    fieldsets = (
        ('اطلاعات کاربری', {
            "fields": (
                'uuid','username', 'first_name', 'last_name','is_staff','password' 
            ),
        }),
        ('اطلاعات ورود و خروج', {
            'fields': ('date_joined','last_login',)
        })
    )
    # Permissions
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ()
        return self.readonly_fields
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return super().has_change_permission(request, obj)

    

class CustomProfileAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('uuid_obj','user', 'national_code','is_complete',) 
    list_display_links = ('user',)
    resource_class = ProfileResource
    list_filter = ('age', 'gender', 'city', 'is_complete')
    search_fields = ('age', 'gender', 'city', 'is_complete')
    list_per_page = 10
    readonly_fields = ['user', 'national_code', 'age', 'gender', 'mobile', 'customer_image', 'is_complete','card_number', 'iban', 'back_money', 'address', 'zipcode','street', 'city']
    # FieldSets
    fieldsets = (
        ('اطلاعات کاربری' , {
            'fields' : ('user', 'national_code','age', 'gender','mobile','is_complete', 'customer_image',)
        }), 
        ('اطلاعات بانکی', {
            'fields' : ('card_number', 'iban', 'back_money')
        }), (
            'اطلاعات آدرس', ({
                'fields' : ('zipcode','street', 'city', 'address', )
            })
        )
    )
    # این دو تابع به ما امکان می‌دهند تا مدیران معمولی نتوانند فیلدهای مشخصی را ویرایش کنند و تنها مدیران سوپری‌یوزر (Superuser) این اجازه را داشته باشند.

    # get_readonly_fields: این تابع مشخص می‌کند که کدام فیلدها برای کاربران قابل ویرایش باشند و کدام‌ها فقط قابل مشاهده باشند. در اینجا، اگر کاربر مورد نظر سوپریوزر باشد، تمامی فیلدها به عنوان فیلدهای قابل مشاهده تعریف شده‌اند.

    # has_change_permission: این تابع بررسی می‌کند که آیا کاربر مورد نظر مجوز تغییر اطلاعات یک آیتم را دارد یا نه. در اینجا، اگر کاربر مورد نظر سوپریوزر باشد، مجوز تغییرات داده می‌شود.

    # این دو تابع به ما کنترل بیشتری بر روی مجوزها و دسترسی‌های کاربران در پنل مدیریتی می‌دهند، به‌طوری‌که ما می‌توانید بر اساس نیازهای خود تنظیمات لازم را انجام دهید.
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ()
        return self.readonly_fields
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return super().has_change_permission(request, obj)
    # UUID obj From CustomUser
    def uuid_obj(self, obj) : 
        return obj.user.uuid
    uuid_obj.short_description = 'UUID کاربر'

    
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(CustomProfileModel,CustomProfileAdmin)