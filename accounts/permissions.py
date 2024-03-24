from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
class IsSuperUser(BasePermission):
  def has_permission(self, request, view):
    if request.user and request.user.is_superuser:
      return True
    else:
      raise PermissionDenied('دسترسی غیر مجاز')
    


class AdminPermission : 
  def get_readonly_fields(self, request, obj=None):
    if request.user.is_superuser:
      return ()
    return self.readonly_fields

  def has_change_permission(self, request, obj=None):
    if request.user.is_superuser:
      return True
    return super().has_change_permission(request, obj)

    # get_readonly_fields: این تابع مشخص می‌کند که کدام فیلدها برای کاربران قابل ویرایش باشند و کدام‌ها فقط قابل مشاهده باشند. در اینجا، اگر کاربر مورد نظر سوپریوزر باشد، تمامی فیلدها به عنوان فیلدهای قابل مشاهده تعریف شده‌اند.

    # has_change_permission: این تابع بررسی می‌کند که آیا کاربر مورد نظر مجوز تغییر اطلاعات یک آیتم را دارد یا نه. در اینجا، اگر کاربر مورد نظر سوپریوزر باشد، مجوز تغییرات داده می‌شود.

    # این دو تابع به ما کنترل بیشتری بر روی مجوزها و دسترسی‌های کاربران در پنل مدیریتی می‌دهند، به‌طوری‌که ما می‌توانید بر اساس نیازهای خود تنظیمات لازم را انجام دهید.