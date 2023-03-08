from rest_framework.views import APIView
from .serializers import LoginSerializer
from django.contrib.auth import authenticate
from .tokengeneratedecode import get_tokens_for_user
from rest_framework.response import Response
from rest_framework import status
from .models import ShopDetails
from .custompermissions import CustomAdminPermission



class LoginSuperAdminEndUserShopAdminShopStaff(APIView):
    '''
    this is login for all roles superadmin,
    eshopadmin, eshopstaff, enduser
    '''
    def post(self, request):
        login_serializer_data = LoginSerializer(request.data)
        if login_serializer_data.validate():
            username = login_serializer_data.data.get('username')
            password = login_serializer_data.data.get('password')
            print(username,password)
            users = authenticate(username=username,password=password)
            if users is not None:
                token = get_tokens_for_user(user=users)
                return Response({'token':token},status=status.HTTP_200_OK)
            return Response({'error':f'{username} and {password} is not correct'},status=status.HTTP_401_UNAUTHORIZED)
        

class SuperAdminDashBord(APIView):
    '''
    superadmin dashbord or graph(bsed on orders)
    '''
    def get(self, request):
        return Response('superadmin dashbord')




class ShopBlcokUnblock(APIView):
    '''
    
    '''
    permission_classes=[CustomAdminPermission]
    def patch(self, request):
        shopid = request.query_params.get('sid')
        if shopid is None:
            return Response({'msg':'shopid is needed'})
        try:
            shop = ShopDetails.objects.get(id=shopid)
        except ShopDetails.DoesNotExist:
            return Response({'error':f'{shopid} is not valid'},status=status.HTTP_400_BAD_REQUEST)
        
        if shop.is_active:
            shop.is_active=False
            shop.save()
            return Response({'response':f'{shop.username} is blocked'},status=status.HTTP_200_OK)
        shop.is_active=True
        shop.save()
        return Response({'response':f'{shop.username} is  Unblocked'},status=status.HTTP_200_OK)
