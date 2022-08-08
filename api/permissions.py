from rest_framework import permissions


class isUserStaff(permissions.BasePermission):
    """
        Custom permission to only allow staff user.
    """

    def has_object_permission(self, request, view, obj):
        """
            function to validate if the user has the permissions
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return request.user.is_staff