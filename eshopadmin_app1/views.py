from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from .serializers import ShopDetailsRegisterSerializer,ShopDetailsLoginSerializer,CreateShopStaffSerializer
from admin_app1.tokens_permissions import get_tokens_for_user,get_decoded_payload,CustomShopAdminPermission
from admin_app1.otp import otp
from .models import ShopDetails,ShopStaff
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework import status
from admin_app1.models import CustomUser
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from eshopadmin_product.models import ShopProducts



@api_view(['POST','GET'])
def register_eshop_admin(request):
    '''
    eshop admin registration
    with otp validations
    '''
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
        if not 'otpnumber' in request.session:
            return Response({'msg':'you canot run this request now'})
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
    '''
    login eshop admin
    '''
    if request.method == 'POST':
        serializer = ShopDetailsLoginSerializer(request.data)
        if serializer.validate():
            username = serializer.data.get('username')
            password = serializer.data.get('password')
            shopadmin = authenticate(username=username,password=password)
            print(shopadmin)
            if shopadmin is not None:
                    token = get_tokens_for_user(user=shopadmin)
                    # login(request,shopadmin)
                    return Response({'token':token,'msg':'login success session start'})
            return Response({'msg':'username and password is not currect'})
            



@api_view(['GET'])
@permission_classes([CustomShopAdminPermission])
@login_required
def logout_eshop_admin(request):
    '''
    logout
    '''
    # logout(request)
    return Response({'msg':'logout successfully'})




class ShopStaffCreateView(APIView):
    '''
    
    '''
    permission_classes = [CustomShopAdminPermission]

    def post(self, request):
        '''
        create new shop staff
        '''
        staffserializer = CreateShopStaffSerializer(data=request.data)
        if staffserializer.is_valid(raise_exception=True):
            payload = get_decoded_payload(request)
            staff = staffserializer.save(payload["user_id"])
            return Response({"msg":f'{staff}'},status=status.HTTP_200_OK)
        return Response({'error':'credentials is not valid'},status=status.HTTP_400_BAD_REQUEST)
    


    def get(self, request):
        '''
        view all shop staff
        '''
        payload = get_decoded_payload(request)
        shopstaff = ShopStaff.objects.filter(shop_id=payload['user_id'])
        staffserializer = CreateShopStaffSerializer(shopstaff,many=True)
        return Response({'staffs':f'{staffserializer.data}'})



class EndUserBlockUnblock(APIView):
    '''
    this method is block user and unblock user
    '''
    permission_classes=[CustomShopAdminPermission]
    def put(self, request):
        id = request.query_params.get('id')
        # print(id)
        try:
            enduser = CustomUser.objects.get(id=id)
        except CustomUser.DoesNotExist:
            return Response({"error":f"{id} is not valid",'or':'check query param'})
        else:
            if enduser.is_active:
                enduser.is_active = False
                enduser.save()
                return Response({"msg":f'blocked {enduser.username}'})
            else:
                enduser.is_active = True
                enduser.save()
                return Response({"msg":f'unblocked {enduser.username}'})


class ProductChageAvailability(APIView):
    '''
    
    '''

    def patch(self, request):
        product_id = request.query_params.get(id)
        try:
            product = ShopProducts.objects.get(id=product_id)
        except ShopProducts.DoesNotExist:
            return Response({'error':f'product_id = {product_id}, is not valid'})
        
        if product.is_available:
            product.is_available = False
            product.save()
            return Response({'msg':f"{product.name} is blocked"})
        product.is_available = True
        product.save()
        return Response({'msg':f'{product.name} is unblocked'})