from rest_framework.permissions import BasePermission

class IsOpsUser(BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated
        if request.user and request.user.is_authenticated:
            # Check if the usertype is 'ops_user'
            return request.user.user_type == 'ops'
        return False

class IsClientUser(BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated
        if request.user and request.user.is_authenticated:
            # Check if the usertype is 'client_user'
            return request.user.user_type == 'client_user'
        return False