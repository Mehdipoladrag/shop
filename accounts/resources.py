# این فایل برای این است که تمام مدل های مورد نیاز را به حالت 
# resource در اورده
# و آن را در ادمین استفاده و بتوانیم دیتا را در قالب فرمت های مختلف استخراج کنیم

from import_export import resources
from accounts.models import CustomUser, CustomProfileModel

class UserResource(resources.ModelResource):
  class Meta:
    model = CustomUser
    fields = ('username', 'first_name', 'last_name', 'email', 'is_active', 'date_joined')


class ProfileResource(resources.ModelResource) : 
  class Meta : 
    model = CustomProfileModel
