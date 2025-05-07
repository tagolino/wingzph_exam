from rest_framework import permissions


class isAdminRole(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        is_allowed = super().has_permission(request, view)
        if is_allowed:
            return request.user.role == "admin"
        return is_allowed
