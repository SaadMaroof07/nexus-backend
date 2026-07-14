from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Sab log kisi ka bhi profile DEKH sakte hain (GET).
    Lekin EDIT/DELETE sirf apna hi profile kar sakta hai.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:  # GET request
            return True
        return obj == request.user  # sirf apna profile edit karne do