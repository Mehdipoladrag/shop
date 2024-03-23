from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
class IsSuperUser(BasePermission):
  def has_permission(self, request, view):
    if request.user and request.user.is_superuser:
      return True
    else:
      raise PermissionDenied('دسترسی غیر مجاز')
