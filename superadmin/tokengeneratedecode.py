from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import BasePermission
from eshop_project.settings import SECRET_KEY
import jwt
from superadmin.models import CustomUser,UsersDetails



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        return token
    



def get_tokens_for_user(user):
    '''
    create custom token
    '''
    refresh = RefreshToken.for_user(user)
    refresh['role']=user.role
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



def get_decoded_payload(request):
    '''
    this function is provide decoded token payload data
    '''
    token = request.headers.get('Authorization').split(' ')[1]
    return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])


def query_param_token_decode(token):
    return jwt.decode(token, SECRET_KEY,algorithms=['HS256'])


def check_jwt_user_id_kwargs_id(request,kwargs):
    user_id = CustomUser.objects.get(username=request.user)
    return user_id.id == kwargs


def check_valid_shop_userid(request,kwargs):
    user = UsersDetails.objects.get(username=request.user)
    return not user.shop.id == kwargs


def check_online_place_order(token,kwargs):
    payload = jwt.decode(token, SECRET_KEY,algorithms=['HS256'])
    user = UsersDetails.objects.get(id=payload['user_id'])
    return not user.shop.id == kwargs['shopid']

def check_not_superadmin(super_admin_id):
    user = CustomUser.objects.get(id=super_admin_id)
    if user.is_superuser:
        return False
    return True
