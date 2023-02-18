from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import BasePermission
from eshop_project.settings import SECRET_KEY
import jwt



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        return token
    


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    refresh['role']=user.role
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class CustomAdminPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == 'admin')
    
class CustomShopAdminPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == 'shopadmin')
    
class CustomShopStaffPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == 'shopstaff')
    
class CustomEndUserPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == 'enduser')
    

def get_decoded_payload(request):
    token = request.headers.get('Authorization').split(' ')[1]
    return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])