from rest_framework import permissions

class SafeMethodsOnlyPermission(permissions.BasePermission):
    """Only can access non-destructive methods (like GET and HEAD)"""
    def has_permission(self, request, view):
        return self.has_object_permission(request, view)

    def has_object_permission(self, request, view, obj=None):
        return request.method in permissions.SAFE_METHODS

class UserCanAddCompanyPermission(SafeMethodsOnlyPermission):
    """Allow everyone which is not a shareholder nor an operator yet to add a company"""
    def has_object_permission(self, request, view, obj=None):
        can_add = False
        if obj is None:
            # Either a list or a create, so no author
            can_add = True
        return can_add or super(UserCanAddCompanyPermission, self).has_object_permission(request, view, obj)

class UserCanAddShareholderPermission(SafeMethodsOnlyPermission):
    """Allow everyone to add a company"""
    def has_object_permission(self, request, view, obj=None):
        can_add = False
        if obj is None:
            # Either a list or a create, so no author
            can_add = True
        return can_add or super(UserCanAddShareholderPermission, self).has_object_permission(request, view, obj)
