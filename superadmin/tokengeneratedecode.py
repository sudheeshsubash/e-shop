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