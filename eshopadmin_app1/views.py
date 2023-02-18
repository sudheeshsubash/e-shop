from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from .serializers import ShopDetailsRegisterSerializer,ShopDetailsLoginSerializer
from admin_app1.tokens_permissions import get_tokens_for_user,CustomShopAdminPermission
from admin_app1.otp import otp
from .models import ShopDetails
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate




@api_view(['POST','GET'])
def register_eshop_admin(request):
    if request.method == 'POST':
        serializer = ShopDetailsRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            otpnumber = otp(phone=serializer.data.get("phone_number"))

            request.session['username'] = serializer.data.get("username")
            request.session['password'] = serializer.data.get("password")
            request.session['email'] = serializer.data.get("email")
            request.session['place'] = serializer.data.get("place")
            request.session['address'] = serializer.data.get("address")
            request.session['ownername'] = serializer.data.get("ownername")
            request.session['phone'] =  serializer.data.get("phone_number")
            request.session['otpnumber'] = otpnumber()

            return Response({"msg":"confim otp"})
        return Response({"msg":"input data is not valid"})

    if request.method == 'GET':
        query_otp = request.query_params
        if int(query_otp.get('otp'))==request.session['otpnumber']:
            shop = ShopDetails.objects.create(
                username = request.session['username'],
                password = make_password(request.session['password']),
                email = request.session['email'],
                place = request.session['place'],
                address = request.session['address'],
                ownername = request.session['ownername'],
                phone_number = request.session['phone'],
                role = 'shopadmin',

            )
            request.session.flush()

            return Response({"msg":f'{shop} successfully created'})
        return Response({"msg":'otp not valid'})



@api_view(['POST'])
def login_eshop_admin(request):

    if request.method == 'POST':
        serializer = ShopDetailsLoginSerializer(request.data)
        if serializer.validate():
            username = serializer.data.get('username')
            password = serializer.data.get('password')
            shopadmin = authenticate(username=username,password=password)
            if shopadmin is not None:
                token = get_tokens_for_user(user=shopadmin)
                # request.session['shopadmin']=shopadmin
                return Response({'token':token,'msg':'login success session start'})
            return Response({'msg':"username and password is not currect"})





@api_view(['GET'])
@permission_classes([CustomShopAdminPermission])
def logout_eshop_admin(request):
    # request.session.flush()
    return Response({'msg':'logout'})