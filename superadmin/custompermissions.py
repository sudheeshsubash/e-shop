from rest_framework.permissions import BasePermission



class CustomAdminPermission(BasePermission):
    '''
    only lsuperadmin can access this token
    '''
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return bool(request.user and request.user.role == 'admin')
        return False


    
class CustomShopAdminPermission(BasePermission):
    '''
    only shopadmin can access this token
    '''
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return bool(request.user and request.user.role == 'shopadmin')
    


class CustomShopStaffPermission(BasePermission):
    '''
    only shopstaff can access this token
    '''
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return bool(request.user and request.user.role == 'shopstaff')
    


class CustomEndUserPermission(BasePermission):
    '''
    end user can access this
    '''
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return bool(request.user and request.user.role == 'enduser')
    
