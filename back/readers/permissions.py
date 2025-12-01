from rest_framework.permissions import BasePermission
from purchasers.utils import can_access_chapter

class CanAccessChapter(BasePermission):
    message = "You don't have permission to access this chapter."

    def has_permission(self, request, view):
        return True
    
    def has_object_permission(self, request, view, obj):
        return can_access_chapter(request.user, obj)